import click

from click_extensions.decorators import catch_exception, print_markers

from tigerhost.api_client import ApiClientResponseError
from tigerhost.utils import decorators


@click.command()
@print_markers
@catch_exception(ApiClientResponseError)
@decorators.store_api_client
@decorators.store_app
@click.pass_context
def get_users(ctx):
    """List the users with access to this app
    """
    app = ctx.obj['app']
    api_client = ctx.obj['api_client']
    owner = api_client.get_application_owner(app)
    collaborators = api_client.get_application_collaborators(app)
    click.echo('Owner: {}'.format(owner))
    click.echo()
    click.echo('Collaborators:')
    for x in collaborators:
        click.echo(x)


@click.command()
@click.argument('username')
@print_markers
@catch_exception(ApiClientResponseError)
@decorators.store_api_client
@decorators.store_app
@click.pass_context
def add_access(ctx, username):
    """Add a user as a collaborator to this app
    """
    app = ctx.obj['app']
    api_client = ctx.obj['api_client']
    api_client.add_application_collaborator(app, username)
    click.echo('Added {user} to {app} as a collaborator.'.format(user=username, app=app))


@click.command()
@click.argument('username')
@print_markers
@catch_exception(ApiClientResponseError)
@decorators.store_api_client
@decorators.store_app
@click.pass_context
def remove_access(ctx, username):
    """Remove a collaborator from this app
    """
    app = ctx.obj['app']
    api_client = ctx.obj['api_client']
    api_client.remove_application_collaborator(app, username)
    click.echo('Removed collaborator {user} from {app}.'.format(user=username, app=app))
