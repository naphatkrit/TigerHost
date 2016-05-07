import click

from click_extensions import private_dir
from click_extensions.commands import bash_complete_command

import deploy

from deploy import settings
from deploy.commands.addons.entry import entry as addons_entry
from deploy.commands.create import create
from deploy.commands.deis.entry import entry as deis_entry
from deploy.commands.destroy import destroy
from deploy.commands.main.entry import entry as main_entry
from deploy.commands.project import project
from deploy.commands.secret import secret
from deploy.commands.secret_clone import secret_clone
from deploy.commands.update import update
from deploy.secret import secret_dir


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=deploy.__version__, prog_name='deploy')
def entry():
    """Commands related to deployment of TigerHost
    """
    private_dir.ensure_private_dir_exists(settings.APP_NAME)
    secret_dir.ensure_secret_dir_exists()


entry.add_command(bash_complete_command(settings.APP_NAME))

entry.add_command(addons_entry, 'addons')
entry.add_command(create)
entry.add_command(deis_entry, 'deis')
entry.add_command(destroy)
entry.add_command(main_entry, 'main')
entry.add_command(project)
entry.add_command(secret)
entry.add_command(secret_clone)
entry.add_command(update)
