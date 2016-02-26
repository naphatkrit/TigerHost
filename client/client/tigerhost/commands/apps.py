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
