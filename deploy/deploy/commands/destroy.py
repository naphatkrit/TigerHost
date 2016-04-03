import click
import subprocess32 as subprocess

from tigerhost.utils.decorators import print_markers

from deploy import settings
from deploy.utils.decorators import require_docker_machine


@click.command()
@print_markers
@require_docker_machine
def destroy():
    subprocess.check_call([settings.APP_NAME, 'main', 'destroy'])
    subprocess.check_call([settings.APP_NAME, 'addons', 'destroy'])
    subprocess.check_call([settings.APP_NAME, 'deis', 'destroy'])
