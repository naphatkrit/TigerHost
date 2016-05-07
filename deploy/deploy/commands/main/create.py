import boto3
import click
import json
import os
import subprocess32 as subprocess
import yaml

from click_extensions import echo_heading
from click_extensions.decorators import print_markers

from deploy import docker_machine, settings
from deploy.project import get_project_path
from deploy.secret import store
from deploy.utils import path_utils
from deploy.utils.decorators import ensure_project_path, require_docker_machine, require_docker_compose
from deploy.utils.utils import parse_shell_for_exports, set_aws_security_group_ingress_rule


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
    docker_machine.check_call(
        ['regenerate-certs', '--force', machine_name])


@click.command()
@click.option('--addon-name', '-a', default='tigerhost-addons-aws', help='The name of the addons server machine. This must be a valid, existing Docker machine. Defaults to tigerhost-addons-aws.')
@click.option('--database', '-d', required=True, help='Postgres URL for TigerHost.')
@click.option('--elastic-ip-id', '-e', required=True, help='Elastic IP allocation ID, used to associate the created machine with.')
@click.option('--instance-type', '-i', default='t2.medium', help='The AWS instance type to use. Defaults to t2.medium.')
@click.option('--name', '-n', default='tigerhost-aws', help='The name of the machine to create. Defaults to tigerhost-aws.')
@click.option('--secret', '-s', required=True, help='Django secret key.')
@print_markers
@ensure_project_path
@require_docker_machine
@require_docker_compose
def create(name, instance_type, database, addon_name, secret, elastic_ip_id):
    """Create a new machine for the main TigerHost server.

    The addon servers machine must already be created.
    """
    project_path = get_project_path()

    # get url, ensures addon machine exists
    echo_heading('Making sure addon machine exists.', marker='-', marker_color='magenta')
    addon_docker_host = docker_machine.get_url(addon_name)
    click.echo('Done.')

    echo_heading('Copying addon machine credentials.', marker='-', marker_color='magenta')
    target_path = os.path.join(project_path, 'web/credentials')
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    docker_machine.retrieve_credentials(addon_name, target_path)
    click.echo('Done.')

    echo_heading('Creating machine {name} with type {type}.'.format(
        name=name, type=instance_type), marker='-', marker_color='magenta')
    if settings.DEBUG:
        docker_machine.check_call(['create', '--driver',
                                   'virtualbox', name])
    else:
        docker_machine.check_call(['create', '--driver',
                                   'amazonec2', '--amazonec2-instance-type', instance_type, name])
        set_aws_security_group_ingress_rule(
            'docker-machine', 0, 65535, '0.0.0.0/0')

        echo_heading(
            'Associating Elastic IP.'.format(name), marker='-', marker_color='magenta')
        click.echo('Done.')
        new_ip = _associate_elastic_ip(name, elastic_ip_id)

        echo_heading(
            'Saving IP {} to docker-machine.'.format(new_ip), marker='-', marker_color='magenta')
        _update_docker_machine_ip(name, new_ip)

    echo_heading('Generating docker-compose file.', marker='-', marker_color='magenta')
    _generate_compose_file(project_path, database, addon_docker_host, secret)
    click.echo('Done.')

    echo_heading('Initializing TigerHost containers.', marker='-', marker_color='magenta')
    env_text = docker_machine.check_output(['env', name])
    env = os.environ.copy()
    env.update(parse_shell_for_exports(env_text))
    subprocess.check_call(['docker-compose', '-f', os.path.join(
        get_project_path(), 'docker-compose.prod.yml'), '-p', settings.MAIN_COMPOSE_PROJECT_NAME, 'up', '-d'], env=env)
    store.set('main__database_url', database)
    store.set('main__django_secret', secret)
    store.set('main__addon_name', addon_name)
    store.set('main__elastic_ip_id', elastic_ip_id)
