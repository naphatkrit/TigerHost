import click
import os
import subprocess32 as subprocess

from tigerhost.utils.decorators import print_markers
from tigerhost.utils.click_utils import echo_with_markers

from deploy import docker_machine, settings
from deploy.commands.main.create import _generate_compose_file
from deploy.project import get_project_path
from deploy.secret import store
from deploy.utils.decorators import ensure_project_path, require_docker_machine
from deploy.utils.utils import parse_shell_for_exports


@click.command()
@click.option('--name', '-n', default='tigerhost-aws', help='The name of the machine to update. Defaults to tigerhost-aws.')
@print_markers
@ensure_project_path
@require_docker_machine
def update(name):
    echo_with_markers('Retrieving server config.', marker='-')
    project_path = get_project_path()
    database = store.get('main__database_url')
    secret = store.get('main__django_secret')
    addon_docker_host = store.get('main__addon_docker_host')
    if database is None or secret is None or addon_docker_host is None:
        raise click.exceptions.ClickException('Server config not found. Was a TigerHost server created with `{} main create`?'.format(settings.APP_NAME))
    click.echo('Done.')

    echo_with_markers('Generating docker-compose file.', marker='-')
    _generate_compose_file(project_path, database, addon_docker_host, secret)
    click.echo('Done.')

    echo_with_markers('Initializing TigerHost containers.', marker='-')
    env_text = docker_machine.check_output(['env', name])
    env = os.environ.copy()
    env.update(parse_shell_for_exports(env_text))
    subprocess.check_call(['docker-compose', '-f', os.path.join(
        get_project_path(), 'docker-compose.prod.yml'), 'up', '-d'], env=env)
