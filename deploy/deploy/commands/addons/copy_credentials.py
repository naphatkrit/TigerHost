import click
import os

from tigerhost.utils.decorators import print_markers

from deploy.project import get_project_path
from deploy.docker_machine import retrieve_credentials
from deploy.utils.decorators import ensure_project_path


@click.command('copy-credentials')
@click.option('--name', '-n', default='tigerhost-addons-aws', help='The name of the machine. Defaults to tigerhost-addons-aws.')
@print_markers
@ensure_project_path
def copy_credentials(name):
    project_path = get_project_path()
    target_path = os.path.join(project_path, 'web/credentials')
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    retrieve_credentials(name, target_path)
