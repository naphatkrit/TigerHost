import click

from tigerhost.api_client import ApiClientResponseError
from tigerhost.utils import decorators


@click.command()
@decorators.print_markers
@decorators.catch_exception(ApiClientResponseError)
@decorators.store_user
@decorators.store_api_client
@click.pass_context
def list_providers(ctx):
    """Show the list of keys for this user.
    """
    api_client = ctx.obj['api_client']
    user = ctx.obj['user']
    providers_info = api_client.get_providers()
    click.echo('{} has access to the following providers:'.format(user.username))
    for p in providers_info['providers']:
        click.echo(p)
    click.echo()
    click.echo('{} is the default provider.'.format(providers_info['default']))
