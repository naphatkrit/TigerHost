import click

from deploy.commands.addons.copy_credentials import copy_credentials
from deploy.commands.addons.create import create
from deploy.commands.addons.destroy import destroy
from deploy.commands.addons.update import update


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def entry():
    pass


entry.add_command(copy_credentials)
entry.add_command(create)
entry.add_command(destroy)
entry.add_command(update)
