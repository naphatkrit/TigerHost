import click
import os
import subprocess32 as subprocess

from click_extensions import echo_heading
from click_extensions.decorators import print_markers

from deploy import docker_machine, settings
from deploy.commands.addons.create import _generate_compose_file
from deploy.project import get_project_path
from deploy.secret import store
from deploy.utils import utils
from deploy.utils.decorators import ensure_project_path, require_docker_machine, require_docker_compose


@click.command()
@click.option('--name', '-n', default='tigerhost-addons-aws', help='The name of the machine to update. Defaults to tigerhost-addons-aws.')
@print_markers
@ensure_project_path
@require_docker_machine
@require_docker_compose
def update(name):
    """Update the addon server.
    """
    echo_heading('Retrieving addons config.', marker='-', marker_color='magenta')
    database = store.get('addon__database_container_name', default=False)
    if database is False:
        raise click.exceptions.ClickException('Addons config not found. Was an addon server created with `{} addons create`?'.format(settings.APP_NAME))
    click.echo('Done.')

    project_path = get_project_path()
    echo_heading('Generating docker-compose file.', marker='-', marker_color='magenta')
    _generate_compose_file(project_path, database)
    click.echo('Done.')

    echo_heading('Updating addons proxy.', marker='-', marker_color='magenta')
    env_text = docker_machine.check_output(['env', name])
    env = os.environ.copy()
    env.update(utils.parse_shell_for_exports(env_text))

    subprocess.check_call(['docker-compose', '-f', os.path.join(
        project_path, 'proxy/docker-compose.prod.yml'), '-p', settings.ADDONS_COMPOSE_PROJECT_NAME, 'build'], env=env)
    subprocess.check_call(['docker-compose', '-f', os.path.join(
        project_path, 'proxy/docker-compose.prod.yml'), '-p', settings.ADDONS_COMPOSE_PROJECT_NAME, 'up', '-d'], env=env)
