import click
import urlparse

from click_extensions import exit_codes
from click_extensions.decorators import catch_exception, print_markers

from tigerhost import settings
from tigerhost.api_client import ApiClient, ApiClientAuthenticationError, ApiClientResponseError
from tigerhost.user import User, save_user, delete_user, has_saved_user
from tigerhost.utils import decorators


_api_key_url = urlparse.urljoin(settings.API_SERVER_URL, 'api/api_key/')


@click.command()
@click.pass_context
@click.option('--username', '-u', default=None, help='Your username (netID)', type=str)
@click.option('--api-key', '-a', default=None, help='The API key optained from {}'.format(_api_key_url), type=str)
@print_markers
@catch_exception(ApiClientResponseError)
def login(ctx, username, api_key):
    """Logs the user in by asking for username and api_key
    """
    if username is None:
        username = click.prompt('Username (netID)')
        click.echo()
    if api_key is None:
        click.echo('Please get your API key from ' +
                   click.style(_api_key_url, underline=True))
        api_key = click.prompt('API key')
        click.echo()
    click.echo('Checking your credentials...', nl=False)

    client = ApiClient(api_server_url=settings.API_SERVER_URL,
                       username=username, api_key=api_key)
    try:
        client.test_api_key()
    except ApiClientAuthenticationError:
        click.secho('invalid', bg='red', fg='black')
        click.echo('Please try again.')
        ctx.exit(code=exit_codes.OTHER_FAILURE)
    else:
        click.secho('OK', bg='green', fg='black')
        user = User(username=username, api_key=api_key)
        save_user(user)


@click.command()
@print_markers
@catch_exception(ApiClientResponseError)
@decorators.store_user
@click.pass_context
def user_info(ctx):
    """Display information about the logged in user.
    """
    user = ctx.obj['user']
    click.echo('Username: {}'.format(user.username))
    click.echo('API key: {}'.format(user.api_key))
    click.echo()
    click.echo('Credentials still valid.')


@click.command()
@print_markers
@catch_exception(ApiClientResponseError)
@click.pass_context
def logout(ctx):
    """Log the user out, deleting the API key.
    """
    if not has_saved_user():
        click.echo('Not logged in.')
        ctx.exit(code=exit_codes.OTHER_FAILURE)
    else:
        delete_user()
        click.echo('Logged out.')
