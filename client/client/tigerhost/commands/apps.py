import click

from tigerhost.api_client import ApiClientResponseError
from tigerhost.utils import decorators


@click.command()
@decorators.print_markers
@decorators.catch_exception(ApiClientResponseError)
@decorators.pass_api_client
def list_apps(api_client):
    """List apps for this user

    @type api_client: tigerhost.api_client.ApiClient
    """
    apps = api_client.get_all_applications()
    for app in apps:
        click.echo(app)


@click.command()
@click.argument('name')
@decorators.print_markers
@decorators.catch_exception(ApiClientResponseError)
@decorators.pass_api_client
def create_app(api_client, name):
    """Create a new app with the specified NAME.
    """
    api_client.create_application(name)
    click.echo('App {} created.'.format(name))


@click.command()
@click.option('--app', '-a', help='Optionally specify which app to work with. Defaults to the current app.')
@decorators.print_markers
@decorators.catch_exception(ApiClientResponseError)
@decorators.pass_api_client
def destroy_app(api_client, app):
    """Delete the current application.
    """
    assert app
    api_client.delete_application(app)
    click.echo('App {} destroyed.'.format(app))
