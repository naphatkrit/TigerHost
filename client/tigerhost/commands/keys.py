import click
import os

from click_extensions.decorators import catch_exception, print_markers

from tigerhost.api_client import ApiClientResponseError
from tigerhost.utils import decorators


@click.command()
@click.argument('name')
@click.argument('path', default='~/.ssh/id_rsa.pub')
@click.option('--backend', '-b', help='The backend to add this key to. Defaults to the default backend.')
@print_markers
@catch_exception(ApiClientResponseError)
@catch_exception(IOError)
@decorators.store_api_client
@click.pass_context
def add_key(ctx, name, path, backend):
    """Add a public key. The NAME is the human readable label to attach
    to this key. PATH is the path to the public key, defaulting to
    ~/.ssh/id_rsa.pub.
    """
    api_client = ctx.obj['api_client']
    path = os.path.expanduser(path)
    with open(path, 'r') as f:
        key = f.read()
    api_client.add_key(name, key, backend)
    if backend is not None:
        click.echo('Added key {} to {}.'.format(name, backend))
    else:
        click.echo('Added key {}.'.format(name))


def _truncate(text):
    length = 20
    dots = '...'
    if len(text) > length * 2 + len(dots):
        return text[:length] + dots + text[-length:]
    else:
        return text


@click.command()
@print_markers
@catch_exception(ApiClientResponseError)
@decorators.store_api_client
@click.pass_context
def list_keys(ctx):
    """Show the list of keys for this user.
    """
    api_client = ctx.obj['api_client']
    first = True
    for backend, keys in api_client.get_keys().iteritems():
        if first:
            first = False
        else:
            click.echo()
        click.echo('backend: {}'.format(backend))
        content = '\n'.join(
            ['{}\n{}'.format(key['key_name'], key['key']) for key in keys])
        click.echo(content)


@click.command()
@click.argument('name')
@click.option('--backend', '-b', help='The backend to remove this key from. Defaults to the default backend.')
@print_markers
@catch_exception(ApiClientResponseError)
@catch_exception(IOError)
@decorators.store_api_client
@click.pass_context
def remove_key(ctx, name, backend):
    """Removes the key with label NAME.
    """
    api_client = ctx.obj['api_client']
    if backend is None:
        backend = api_client.get_backends()['default']
    api_client.remove_key(name, backend)
    click.echo('Key {} removed from {}.'.format(name, backend))
