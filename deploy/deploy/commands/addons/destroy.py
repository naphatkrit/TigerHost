import click
import subprocess32 as subprocess

from tigerhost.utils.click_utils import echo_with_markers
from tigerhost.utils.decorators import print_markers


@click.command()
@click.option('--name', '-n', default='tigerhost-addons-aws', help='The name of the machine to destroy. Defaults to tigerhost-addons-aws.')
@print_markers
def destroy(name):
    # TODO ensure docker machine is installed
    echo_with_markers('Destroying machine {name}.'.format(name=name), marker='-')
    subprocess.check_call(['docker-machine', 'rm', '-y', name])
