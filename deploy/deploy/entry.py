import click

from tigerhost import private_dir

import deploy

from deploy import settings
from deploy.commands.addons.entry import entry as addons_entry
from deploy.commands.deis.entry import entry as deis_entry
from deploy.commands.main.entry import entry as main_entry


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=deploy.__version__, prog_name='deploy')
def entry():
    private_dir.ensure_private_dir_exists(settings.APP_NAME)


entry.add_command(addons_entry, 'addons')
entry.add_command(deis_entry, 'deis')
entry.add_command(main_entry, 'main')
