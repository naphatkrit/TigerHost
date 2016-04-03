import click
import os
import subprocess32 as subprocess

from tigerhost.utils.click_utils import echo_with_markers
from tigerhost.utils.decorators import print_markers

from deploy import settings
from deploy.commands.addons.create import _generate_compose_file
from deploy.project import get_project_path
from deploy.secret import store
from deploy.utils import utils
from deploy.utils.decorators import ensure_project_path, require_docker_machine


@click.command()
@click.option('--name', '-n', default='tigerhost-addons-aws', help='The name of the machine to update. Defaults to tigerhost-addons-aws.')
@print_markers
@ensure_project_path
@require_docker_machine
def update(name):
    echo_with_markers('Retrieving addons config.', marker='-')
    database = store.get('addon__database_container_name', default=False)
    if database is False:
        raise click.exceptions.ClickException('Addons config not found. Was an addon server created with `{} addons create`?'.format(settings.APP_NAME))
    click.echo('Done.')

    project_path = get_project_path()
    echo_with_markers('Generating docker-compose file.', marker='-')
    _generate_compose_file(project_path, database)
    click.echo('Done.')

    echo_with_markers('Updating addons proxy.', marker='-')
    env_text = subprocess.check_output(['docker-machine', 'env', name])
    env = os.environ.copy()
    env.update(utils.parse_shell_for_exports(env_text))

    subprocess.check_call(['docker-compose', '-f', os.path.join(
        project_path, 'proxy/docker-compose.prod.yml'), 'up', '-d'], env=env)
