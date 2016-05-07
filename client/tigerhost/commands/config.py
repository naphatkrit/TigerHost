import click

from click_extensions import exit_codes
from click_extensions.decorators import catch_exception, print_markers

from tigerhost.api_client import ApiClientResponseError
from tigerhost.utils import decorators


@click.command()
@print_markers
@catch_exception(ApiClientResponseError)
@decorators.store_api_client
@decorators.store_app
@click.pass_context
def list_config(ctx):
    """List the config variables for this app.
    """
    app = ctx.obj['app']
    api_client = ctx.obj['api_client']
    config_vars = api_client.get_application_env_variables(app)
    for name, value in config_vars.iteritems():
        click.echo('{name}={value}'.format(name=name, value=value))


@click.command()
@click.argument('variables', nargs=-1, required=True)
@print_markers
@catch_exception(ApiClientResponseError)
@decorators.store_api_client
@decorators.store_app
@click.pass_context
def set_config(ctx, variables):
    """Set config variables. Variables are passed in the form NAME=value.
    Multiple variables can be set at once; they are passed in space separated.
    """
    bindings = {}
    for pair in variables:
        pair = pair.split('=', 1)
        if len(pair) != 2:
            click.echo('Variables must be passed in the format NAME=value.')
            ctx.exit(code=exit_codes.OTHER_FAILURE)
        name, value = pair
        if value == '':
            value = None
        bindings[name] = value
    app = ctx.obj['app']
    api_client = ctx.obj['api_client']
    api_client.set_application_env_variables(app, bindings)
    click.echo('The following variables set successfully:')
    for name, value in bindings.iteritems():
        click.echo('{name}={value}'.format(
            name=name, value=value if value else ''))


@click.command()
@click.argument('variables', nargs=-1, required=True)
@print_markers
@catch_exception(ApiClientResponseError)
@decorators.store_api_client
@decorators.store_app
@click.pass_context
def unset_config(ctx, variables):
    """Unset config variables. Multiple variables can be unset at
    the same time, passed in space separated.
    """
    bindings = {key: None for key in variables}
    app = ctx.obj['app']
    api_client = ctx.obj['api_client']
    api_client.set_application_env_variables(app, bindings)
    click.echo('The following variables unset successfully:')
    for name, value in bindings.iteritems():
        click.echo('{name}'.format(name=name))
