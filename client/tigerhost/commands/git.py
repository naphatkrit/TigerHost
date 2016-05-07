import click

from click_extensions.decorators import catch_exception, print_markers

from tigerhost import settings
from tigerhost.api_client import ApiClientResponseError
from tigerhost.utils import decorators
from tigerhost.vcs.base import CommandError


@click.command()
@click.option('--app', '-a', required=True, help='The app to work with')
@click.option('--remote', '-r', default=None, help='The git remote to create')
@print_markers
@catch_exception(ApiClientResponseError)
@catch_exception(CommandError)
@decorators.store_api_client
@decorators.store_vcs
@click.pass_context
def add_remote(ctx, app, remote):
    """Add a git remote to an app repo.
    """
    if remote is None:
        remote = settings.APP_NAME
    api_client = ctx.obj['api_client']
    vcs = ctx.obj['vcs']
    remote_url = api_client.get_application_git_remote(app)
    vcs.add_remote(remote, remote_url)
    click.echo('Successfully set remote {remote} to {url}'.format(
        remote=remote, url=remote_url))
