import click
import os
import random
import string
import subprocess32 as subprocess
import yaml

from tigerhost.utils.decorators import print_markers
from tigerhost.utils.click_utils import echo_with_markers

from tigerhostctl.project import get_project_path
from tigerhostctl.utils import click_utils
from tigerhostctl.utils.decorators import ensure_project_path
from tigerhostctl.utils.utils import parse_shell_for_exports


def _get_secret():
    click.echo('Django needs a secret key.')
    choice = click_utils.prompt_choices([
        'Generate a random secret key.',
        'Enter a secret key.'
    ])
    if choice == 0:
        rand = random.SystemRandom()
        secret = ''.join(rand.choice(string.ascii_letters +
                                     string.digits) for _ in range(100))
        click.echo('Generated secret: {}'.format(secret))
        click.echo(
            'Please save this somewhere safe. You will need it to update TigerHost.')
        click.confirm('Continue?', default=True, abort=True)
    else:
        # TODO only accept [a-zA-Z0-9]
        secret = click.prompt('Secret', type=str, confirmation_prompt=True)
    return secret


def _generate_compose_file(project_path, database_url, addon_docker_host, secret):
    with open(os.path.join(project_path, 'docker-compose.prod.template.yml'), 'r') as f:
        data = yaml.safe_load(f)
    for d in (data['services']['web'], data['services']['worker']):
        d['environment']['DOCKER_HOST'] = addon_docker_host
        d['environment']['DATABASE_URL'] = database_url
        d['environment']['SECRET'] = secret
    with open(os.path.join(project_path, 'docker-compose.prod.yml'), 'w') as f:
        yaml.safe_dump(data, f)


@click.command()
@click.option('--name', '-n', default='tigerhost-aws', help='The name of the machine to create. Defaults to tigerhost-aws.')
@click.option('--instance-type', '-i', default='t2.medium', help='The AWS instance type to use. Defaults to t2.medium.')
@click.option('--database', '-d', required=True, help='Postgres URL for TigerHost.')
@click.option('--addon-docker-host', '-a', required=True, help='The URL for the addon docker host. This is DOCKER_HOST from running `docker-machine env {machine_name}`')
@click.option('--secret', '-s', default=None, help='Django secret key.')
@print_markers
@ensure_project_path
def create(name, instance_type, database, addon_docker_host, secret):
    if secret is None:
        secret = _get_secret()
    project_path = get_project_path()

    # TODO elastic IP
    echo_with_markers('Creating machine {name} with type {type}.'.format(
        name=name, type=instance_type), marker='-')
    subprocess.check_call(['docker-machine', 'create', '--driver',
                           'amazonec2', '--amazonec2-instance-type', instance_type, name])

    echo_with_markers('Generating docker-compose file.', marker='-')
    _generate_compose_file(project_path, database, addon_docker_host, secret)
    click.echo('Done.')

    echo_with_markers('Initializing TigerHost containers.', marker='-')
    env_text = subprocess.check_output(['docker-machine', 'env', name])
    env = os.environ.copy()
    env.update(parse_shell_for_exports(env_text))
    subprocess.check_call(['docker-compose', '-f', os.path.join(
        get_project_path(), 'docker-compose.prod.yml'), 'up', '-d'], env=env)
