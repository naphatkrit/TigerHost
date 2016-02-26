import click
import os

from tigerhost.api_client import ApiClientResponseError
from tigerhost.utils import decorators


@click.command()
@click.argument('name')
@click.argument('path', default='~/.ssh/id_rsa.pub')
@decorators.print_markers
@decorators.catch_exception(ApiClientResponseError)
@decorators.catch_exception(IOError)
@decorators.pass_api_client
def add_key(api_client, name, path):
    """Add a public key. The NAME is the human readable label to attach
    to this key. PATH is the path to the public key, defaulting to
    ~/.ssh/id_rsa.pub.
    """
    path = os.path.expanduser(path)
    with open(path, 'r') as f:
        key = f.read()
    api_client.add_key(name, key)
    click.echo('Added key {}.'.format(name))


def _truncate(text):
    length = 20
    dots = '...'
    if len(text) > length * 2 + len(dots):
        return text[:length] + dots + text[-length:]
    else:
        return text


@click.command()
@decorators.print_markers
@decorators.catch_exception(ApiClientResponseError)
@decorators.pass_api_client
def list_keys(api_client):
    """Show the list of keys for this user.
    """
    keys = api_client.get_keys()
    first = True
    for key in keys:
        if first:
            first = False
        else:
            click.echo()
        click.echo(key['key_name'].strip())
        click.echo(_truncate(key['key'].strip()))


@click.command()
@click.argument('name')
@decorators.print_markers
@decorators.catch_exception(ApiClientResponseError)
@decorators.catch_exception(IOError)
@decorators.pass_api_client
def remove_key(api_client, name):
    """Removes the key with label NAME.
    """
    api_client.remove_key(name)
    click.echo('Key {} removed.'.format(name))
