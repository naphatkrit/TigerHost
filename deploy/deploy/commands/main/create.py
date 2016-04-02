import boto3
import click
import json
import os
import subprocess32 as subprocess
import yaml

from tigerhost.utils.decorators import print_markers
from tigerhost.utils.click_utils import echo_with_markers

from deploy import settings
from deploy.project import get_project_path
from deploy.secret.docker_machine import store_credentials
from deploy.utils import path_utils
from deploy.utils.decorators import ensure_project_path
from deploy.utils.utils import parse_shell_for_exports


def _generate_compose_file(project_path, database_url, addon_docker_host, secret):
    with open(os.path.join(project_path, 'docker-compose.prod.template.yml'), 'r') as f:
        data = yaml.safe_load(f)
    for d in (data['services']['web'], data['services']['worker']):
        d['environment']['DOCKER_HOST'] = addon_docker_host
        d['environment']['DATABASE_URL'] = database_url
        d['environment']['SECRET'] = secret
    with open(os.path.join(project_path, 'docker-compose.prod.yml'), 'w') as f:
        yaml.safe_dump(data, f)


def _associate_elastic_ip(machine_name, elastic_ip_id):
    ec2 = boto3.resource('ec2')
    instance = list(ec2.instances.filter(Filters=[
        {
            'Name': 'tag:Name',
            'Values': [machine_name]
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running'],
        },
    ]).limit(1))[0]
    instance_id = instance.instance_id
    addr = ec2.VpcAddress(elastic_ip_id)
    addr.associate(InstanceId=instance_id)
    return addr.public_ip


def _update_docker_machine_ip(machine_name, new_ip):
    path = path_utils.docker_machine_path(machine_name)
    config_path = os.path.join(path, 'config.json')
    with open(config_path, 'r') as f:
        data = json.load(f)
    data['Driver']['IPAddress'] = new_ip
    with open(config_path, 'w') as f:
        json.dump(data, f)
    subprocess.check_call(
        ['docker-machine', 'regenerate-certs', '--force', machine_name])


@click.command()
@click.option('--addon-docker-host', '-a', required=True, help='The URL for the addon docker host. This is DOCKER_HOST from running `docker-machine env {machine_name}`')
@click.option('--database', '-d', required=True, help='Postgres URL for TigerHost.')
@click.option('--elastic-ip-id', '-e', required=True, help='Elastic IP allocation ID, used to associate the created machine with.')
@click.option('--instance-type', '-i', default='t2.medium', help='The AWS instance type to use. Defaults to t2.medium.')
@click.option('--name', '-n', default='tigerhost-aws', help='The name of the machine to create. Defaults to tigerhost-aws.')
@click.option('--secret', '-s', required=True, help='Django secret key.')
@print_markers
@ensure_project_path
def create(name, instance_type, database, addon_docker_host, secret, elastic_ip_id):
    project_path = get_project_path()

    echo_with_markers('Creating machine {name} with type {type}.'.format(
        name=name, type=instance_type), marker='-')
    if settings.DEBUG:
        subprocess.check_call(['docker-machine', 'create', '--driver',
                               'virtualbox', name])
    else:
        subprocess.check_call(['docker-machine', 'create', '--driver',
                               'amazonec2', '--amazonec2-instance-type', instance_type, name])

        echo_with_markers(
            'Associating Elastic IP.'.format(name), marker='-')
        click.echo('Done.')
        new_ip = _associate_elastic_ip(name, elastic_ip_id)

        echo_with_markers(
            'Saving IP {} to docker-machine.'.format(new_ip), marker='-')
        _update_docker_machine_ip(name, new_ip)

    store_credentials(name)

    echo_with_markers('Generating docker-compose file.', marker='-')
    _generate_compose_file(project_path, database, addon_docker_host, secret)
    click.echo('Done.')

    echo_with_markers('Initializing TigerHost containers.', marker='-')
    env_text = subprocess.check_output(['docker-machine', 'env', name])
    env = os.environ.copy()
    env.update(parse_shell_for_exports(env_text))
    subprocess.check_call(['docker-compose', '-f', os.path.join(
        get_project_path(), 'docker-compose.prod.yml'), 'up', '-d'], env=env)
