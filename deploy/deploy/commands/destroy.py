import click
import subprocess32 as subprocess

from click_extensions.decorators import print_markers

from deploy import settings
from deploy.utils.decorators import require_docker_machine


@click.command()
@print_markers
@require_docker_machine
def destroy():
    """A shortcut to destroy the main TigerHost server, the addons server,
    and the Deis cluster, in that order.
    """
    subprocess.check_call([settings.APP_NAME, 'main', 'destroy'])
    subprocess.check_call([settings.APP_NAME, 'addons', 'destroy'])
    subprocess.check_call([settings.APP_NAME, 'deis', 'destroy'])
