import click

from click_extensions.decorators import catch_exception, print_markers

from tigerhost.api_client import ApiClientResponseError
from tigerhost.utils import decorators


_available_colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']


@click.command()
@click.option('--num', '-n', type=int, help='The number of lines to display')
@print_markers
@catch_exception(ApiClientResponseError)
@decorators.store_api_client
@decorators.store_app
@click.pass_context
def get_logs(ctx, num):
    """Display the application logs.
    """
    app = ctx.obj['app']
    api_client = ctx.obj['api_client']
    colors = dict()
    logs = api_client.get_application_logs(app, lines=num)
    for log in reversed(logs):
        if log['process'] not in colors:
            index = len(colors)
            colors[log['process']] = _available_colors[index % len(_available_colors)]
    for log in logs:
        color = colors[log['process']]
        header = click.style('{timestamp} {app_name}[{process}]:'.format(
            timestamp=log['timestamp'],
            app_name=log['app'],
            process=log['process'],
        ), fg=color)
        click.echo('{header} {message}'.format(header=header, message=log['message']))
