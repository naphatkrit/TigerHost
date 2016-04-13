import click

from deploy.commands.main.configure_dns import configure_dns
from deploy.commands.main.create import create
from deploy.commands.main.destroy import destroy
from deploy.commands.main.update import update


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def entry():
    """This is a group of commands for managing the main TigerHost server.
    """
    pass


entry.add_command(configure_dns)
entry.add_command(create)
entry.add_command(destroy)
entry.add_command(update)
