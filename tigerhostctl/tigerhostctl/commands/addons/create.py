import click
import os
import subprocess32 as subprocess
import yaml

from tigerhost.utils.click_utils import echo_with_markers
from tigerhost.utils.decorators import print_markers

from tigerhostctl.project import get_project_path
from tigerhostctl.utils import utils
from tigerhostctl.utils.decorators import ensure_project_path


def _generate_compose_file(project_path):
    with open(os.path.join(project_path, 'proxy/docker-compose.prod.template.yml'), 'r') as f:
        data = yaml.safe_load(f)
    with open(os.path.join(project_path, 'proxy/docker-compose.prod.yml'), 'w') as f:
        yaml.safe_dump(data, f)


@click.command()
@click.option('--name', '-n', default='tigerhost-addons-aws', help='The name of the machine to create. Defaults to tigerhost-addons-aws.')
@click.option('--instance-type', '-i', default='t2.large', help='The AWS instance type to use. Defaults to t2.large.')
@print_markers
@ensure_project_path
def create(name, instance_type):
    # TODO ensure docker machine is installed
    echo_with_markers('Creating machine {name} with type {type}.'.format(
        name=name, type=instance_type), marker='-')
    subprocess.check_call(
        ['docker-machine', 'create', '--driver', 'amazonec2', '--amazonec2-instance-type', instance_type, name])

    project_path = get_project_path()

    echo_with_markers('Generating docker-compose file.', marker='-')
    _generate_compose_file(project_path)

    echo_with_markers('Instantiating addons proxy.', marker='-')
    env_text = subprocess.check_output(['docker-machine', 'env', name])
    env = os.environ.copy()
    env.update(utils.parse_shell_for_exports(env_text))

    subprocess.check_call(['docker-compose', '-f', os.path.join(
        project_path, 'proxy/docker-compose.prod.yml'), 'up', '-d'], env=env)
