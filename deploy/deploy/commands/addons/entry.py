import click

from deploy.commands.addons.create import create
from deploy.commands.addons.destroy import destroy
from deploy.commands.addons.update import update


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def entry():
    """This is a group of commands for managing the addons server.
    """
    pass


entry.add_command(create)
entry.add_command(destroy)
entry.add_command(update)
