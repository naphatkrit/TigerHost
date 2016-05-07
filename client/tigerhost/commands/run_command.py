import click

from click_extensions.decorators import catch_exception, print_markers

from tigerhost.api_client import ApiClientResponseError
from tigerhost.utils import decorators


@click.command()
@click.argument('command', nargs=-1, required=True)
@print_markers
@catch_exception(ApiClientResponseError)
@decorators.store_api_client
@decorators.store_app
@click.pass_context
def run_one_off(ctx, command):
    """Run a one-off command for this application.
    """
    app = ctx.obj['app']
    api_client = ctx.obj['api_client']
    command = ' '.join(command)
    click.echo('Running {command} on {app}. This may take a while.'.format(command=command, app=app))
    result = api_client.run_command(app, command)
    click.echo(result['output'])
    ctx.exit(code=result['exit_code'])
