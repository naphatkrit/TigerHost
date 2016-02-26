import click

import tigerhost

from tigerhost.commands import apps
from tigerhost.commands.login import login
from tigerhost.private_dir import ensure_private_dir_exists


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=tigerhost.__version__, prog_name='TigerHost')
def entry():
    ensure_private_dir_exists()

entry.add_command(login)
entry.add_command(apps.list_apps, name='apps')
