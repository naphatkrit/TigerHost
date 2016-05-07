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
def list_domains(ctx):
    """List the domains associated with this app.
    """
    app = ctx.obj['app']
    api_client = ctx.obj['api_client']
    domains = api_client.get_application_domains(app)
    for x in domains:
        click.echo(x)


@click.command()
@click.argument('domain', required=True)
@print_markers
@catch_exception(ApiClientResponseError)
@decorators.store_api_client
@decorators.store_app
@click.pass_context
def add_domain(ctx, domain):
    """Add a new domain to this application
    """
    app = ctx.obj['app']
    api_client = ctx.obj['api_client']
    api_client.add_application_domain(app, domain)
    click.echo('Added {domain} to {app}'.format(domain=domain, app=app))


@click.command()
@click.argument('domain', required=True)
@print_markers
@catch_exception(ApiClientResponseError)
@decorators.store_api_client
@decorators.store_app
@click.pass_context
def remove_domain(ctx, domain):
    """Remove a domain from this application
    """
    app = ctx.obj['app']
    api_client = ctx.obj['api_client']
    api_client.remove_application_domain(app, domain)
    click.echo('Removed {domain} from {app}'.format(domain=domain, app=app))
