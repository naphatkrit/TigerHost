import click

from tigerhost import private_dir

import tigerhostctl

from tigerhostctl import settings
from tigerhostctl.commands.addons.entry import entry as addons_entry
from tigerhostctl.commands.deis.entry import entry as deis_entry


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=tigerhostctl.__version__, prog_name='TigerHostCtl')
def entry():
    private_dir.ensure_private_dir_exists(settings.APP_NAME)


entry.add_command(addons_entry, 'addons')
entry.add_command(deis_entry, 'deis')
