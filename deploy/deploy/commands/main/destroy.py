import click

from tigerhost.utils.click_utils import echo_with_markers
from tigerhost.utils.decorators import print_markers

from deploy import docker_machine
from deploy.secret import store
from deploy.utils.decorators import require_docker_machine


@click.command()
@click.option('--name', '-n', default='tigerhost-aws', help='The name of the machine to destroy. Defaults to tigerhost-addons-aws.')
@print_markers
@require_docker_machine
def destroy(name):
    # TODO ensure docker machine is installed
    echo_with_markers('Destroying machine {name}.'.format(name=name), marker='-')
    docker_machine.check_call(['rm', '-y', name])
    store.unset('main__database_url')
    store.unset('main__django_secret')
    store.unset('main__addon_name')
    store.unset('main__elastic_ip_id')
