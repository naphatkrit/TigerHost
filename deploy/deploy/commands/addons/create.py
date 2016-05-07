import click
import os
import subprocess32 as subprocess
import yaml

from click_extensions import echo_heading
from click_extensions.decorators import print_markers

from deploy import docker_machine, settings
from deploy.secret import store
from deploy.project import get_project_path
from deploy.utils import utils
from deploy.utils.decorators import ensure_project_path, require_docker_machine, require_docker_compose


def _generate_compose_file(project_path, database):
    with open(os.path.join(project_path, 'proxy/docker-compose.prod.template.yml'), 'r') as f:
        data = yaml.safe_load(f)
    if database is not None:
        data['services'][database] = {
            'image': 'postgres:9.5',
            'environment': {
                'POSTGRES_USER': database,
            },
        }
    with open(os.path.join(project_path, 'proxy/docker-compose.prod.yml'), 'w') as f:
        yaml.safe_dump(data, f)


@click.command()
@click.option('--name', '-n', default='tigerhost-addons-aws', help='The name of the machine to create. Defaults to tigerhost-addons-aws.')
@click.option('--instance-type', '-i', default='t2.large', help='The AWS instance type to use. Defaults to t2.large.')
@click.option('--database', '-d', default=None, help='Database container name, if a database container is to be created. By default, does not create a database container.')
@click.pass_context
@print_markers
@ensure_project_path
@require_docker_machine
@require_docker_compose
def create(ctx, name, instance_type, database):
    """Create machine for the addon server.
    """
    # TODO verify that database is [a-zA-Z0-9_]
    echo_heading('Creating machine {name} with type {type}.'.format(
        name=name, type=instance_type), marker='-', marker_color='magenta')
    if settings.DEBUG:
        docker_machine.check_call(
            ['create', '--driver', 'virtualbox', name])
    else:
        docker_machine.check_call(
            ['create', '--driver', 'amazonec2', '--amazonec2-instance-type', instance_type, name])
        utils.set_aws_security_group_ingress_rule('docker-machine', 0, 65535, '0.0.0.0/0')

    project_path = get_project_path()

    echo_heading('Generating docker-compose file.', marker='-', marker_color='magenta')
    _generate_compose_file(project_path, database)

    echo_heading('Instantiating addons proxy.', marker='-', marker_color='magenta')
    env_text = docker_machine.check_output(['env', name])
    env = os.environ.copy()
    env.update(utils.parse_shell_for_exports(env_text))

    subprocess.check_call(['docker-compose', '-f', os.path.join(
        project_path, 'proxy/docker-compose.prod.yml'), '-p', settings.ADDONS_COMPOSE_PROJECT_NAME, 'up', '-d'], env=env)

    store.set('addon__database_container_name', database)
