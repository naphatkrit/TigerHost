import click
import datetime
import time

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
            status=x['state']))


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
    click.echo('Name: {}'.format(result['addon']['display_name']))
    click.echo(result['message'])


@click.command()
@click.argument('addon', required=True)
@click.option('--interval', '-i', type=int, default=30, help='The polling interval in seconds.')
@decorators.print_markers
@decorators.catch_exception(ApiClientResponseError)
@decorators.store_api_client
@decorators.store_app
@click.pass_context
def wait_addon(ctx, addon, interval):
    """Waits until an addon becomes ready to use.
    """
    app = ctx.obj['app']
    api_client = ctx.obj['api_client']
    ready = False
    while not ready:
        addon_obj = api_client.get_application_addon(app, addon)
        if addon_obj['state'] == 'ready':
            ready = True
        else:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            click.echo(
                '{} - Current status: {}'.format(timestamp, addon_obj['state']))
            time.sleep(interval)
    click.echo('{} is ready for use!'.format(addon))


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
