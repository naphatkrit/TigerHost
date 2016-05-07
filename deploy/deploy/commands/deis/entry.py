import click

from click_extensions import private_dir

from deploy import settings
from deploy.commands.deis.configure_dns import configure_dns
from deploy.commands.deis.create import create
from deploy.commands.deis.create_admin import create_admin
from deploy.commands.deis.destroy import destroy


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def entry():
    """This is a group of commands for managing the Deis cluster.
    """
    private_dir.ensure_private_dir_exists(settings.APP_NAME)


entry.add_command(configure_dns)
entry.add_command(create)
entry.add_command(create_admin)
entry.add_command(destroy)
