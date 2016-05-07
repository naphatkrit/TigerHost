import click

from click_extensions.decorators import catch_exception, print_markers

from tigerhost.api_client import ApiClientResponseError
from tigerhost.utils import decorators


@click.command()
@print_markers
@catch_exception(ApiClientResponseError)
@decorators.store_user
@decorators.store_api_client
@click.pass_context
def list_backends(ctx):
    """Show the list of keys for this user.
    """
    api_client = ctx.obj['api_client']
    user = ctx.obj['user']
    backends_info = api_client.get_backends()
    click.echo('{} has access to the following backends:'.format(user.username))
    for p in backends_info['backends']:
        click.echo(p)
    click.echo()
    click.echo('{} is the default backend.'.format(backends_info['default']))
