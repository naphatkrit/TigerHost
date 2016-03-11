import click

from tigerhost.api_client import ApiClientResponseError
from tigerhost.utils import decorators


@click.command()
@decorators.print_markers
@decorators.catch_exception(ApiClientResponseError)
@decorators.store_api_client
@decorators.store_app
@click.pass_context
def list_addons(ctx):
    """List addons installed for this app.
    """
    app = ctx.obj['app']
    api_client = ctx.obj['api_client']
    addons = api_client.get_application_addons(app)
    for x in addons:
        click.echo('{name} - {addon} - {status}'.format(
            name=x['display_name'],
            addon=x['provider_name'],
            status=x['status']))


@click.command()
@click.argument('addon', required=True)
@decorators.print_markers
@decorators.catch_exception(ApiClientResponseError)
@decorators.store_api_client
@decorators.store_app
@click.pass_context
def create_addon(ctx, addon):
    """Create a new addon for this app.
    """
    app = ctx.obj['app']
    api_client = ctx.obj['api_client']
    result = api_client.create_application_addon(app, addon)
    click.echo('Name: {}'.format(result['name']))
    click.echo(result['message'])


@click.command()
@click.argument('addon_name', required=True)
@decorators.print_markers
@decorators.catch_exception(ApiClientResponseError)
@decorators.store_api_client
@decorators.store_app
@click.pass_context
def delete_addon(ctx, addon_name):
    """Delete an addon from this app.
    """
    app = ctx.obj['app']
    api_client = ctx.obj['api_client']
    result = api_client.delete_application_addon(app, addon_name)
    click.echo('{} deleted.'.format(addon_name))
    click.echo(result['message'])
