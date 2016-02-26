import click

import tigerhost

from tigerhost.commands import apps, keys
from tigerhost.commands.user import login, user_info, logout
from tigerhost.private_dir import ensure_private_dir_exists


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=tigerhost.__version__, prog_name='TigerHost')
def entry():
    ensure_private_dir_exists()

entry.add_command(login)
entry.add_command(logout)
entry.add_command(user_info, name='user:info')
entry.add_command(apps.list_apps, name='apps')
entry.add_command(keys.add_key, name='keys:add')
entry.add_command(keys.list_keys, name='keys')
entry.add_command(keys.remove_key, name='keys:remove')
