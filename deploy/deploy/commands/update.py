import click
import subprocess32 as subprocess

from click_extensions.decorators import print_markers

from deploy import settings
from deploy.utils.decorators import ensure_project_path, require_docker_machine, require_docker_compose


@click.command()
@print_markers
@ensure_project_path
@require_docker_machine
@require_docker_compose
def update():
    """This is a shortcut to update the addons server and the main server,
    in that order.
    """
    subprocess.check_call([settings.APP_NAME, 'addons', 'update'])
    subprocess.check_call([settings.APP_NAME, 'main', 'update'])
