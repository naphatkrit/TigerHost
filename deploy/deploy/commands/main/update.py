import click
import os
import subprocess32 as subprocess

from click_extensions import echo_heading
from click_extensions.decorators import print_markers

from deploy import docker_machine, settings
from deploy.commands.main.create import _generate_compose_file
from deploy.project import get_project_path
from deploy.secret import store
from deploy.utils.decorators import ensure_project_path, require_docker_machine, require_docker_compose
from deploy.utils.utils import parse_shell_for_exports


@click.command()
@click.option('--name', '-n', default='tigerhost-aws', help='The name of the machine to update. Defaults to tigerhost-aws.')
@print_markers
@ensure_project_path
@require_docker_machine
@require_docker_compose
def update(name):
    """Update the main TigerHost server. This also updates the documentation.
    """
    echo_heading('Retrieving server config.', marker='-', marker_color='magenta')
    project_path = get_project_path()
    database = store.get('main__database_url')
    secret = store.get('main__django_secret')
    addon_name = store.get('main__addon_name')
    if database is None or secret is None or addon_name is None:
        raise click.exceptions.ClickException('Server config not found. Was a TigerHost server created with `{} main create`?'.format(settings.APP_NAME))
    click.echo('Done.')

    echo_heading('Making sure addon machine exists.', marker='-', marker_color='magenta')
    addon_docker_host = docker_machine.get_url(addon_name)
    click.echo('Done.')

    echo_heading('Copying addon machine credentials.', marker='-', marker_color='magenta')
    target_path = os.path.join(project_path, 'web/credentials')
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    docker_machine.retrieve_credentials(addon_name, target_path)
    click.echo('Done.')

    echo_heading('Generating docker-compose file.', marker='-', marker_color='magenta')
    _generate_compose_file(project_path, database, addon_docker_host, secret)
    click.echo('Done.')

    echo_heading('Initializing TigerHost containers.', marker='-', marker_color='magenta')
    env_text = docker_machine.check_output(['env', name])
    env = os.environ.copy()
    env.update(parse_shell_for_exports(env_text))
    subprocess.check_call(['docker-compose', '-f', os.path.join(
        get_project_path(), 'docker-compose.prod.yml'), '-p', settings.MAIN_COMPOSE_PROJECT_NAME, 'build'], env=env)
    subprocess.check_call(['docker-compose', '-f', os.path.join(
        get_project_path(), 'docker-compose.prod.yml'), '-p', settings.MAIN_COMPOSE_PROJECT_NAME, 'up', '-d'], env=env)
