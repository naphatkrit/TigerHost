import click
import subprocess32 as subprocess

from tigerhost.utils.click_utils import echo_with_markers
from tigerhost.utils.decorators import print_markers

from deploy.secret import store


@click.command()
@click.option('--name', '-n', default='tigerhost-aws', help='The name of the machine to destroy. Defaults to tigerhost-addons-aws.')
@print_markers
def destroy(name):
    # TODO ensure docker machine is installed
    echo_with_markers('Destroying machine {name}.'.format(name=name), marker='-')
    subprocess.check_call(['docker-machine', 'rm', '-y', name])
    store.unset('main__database_url')
    store.unset('main__django_secret')
    store.unset('main__addon_docker_host')
    store.unset('main__elastic_ip_id')
