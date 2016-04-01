import click

from tigerhost import private_dir

from deploy import settings
from deploy.commands.deis.create import create
from deploy.commands.deis.destroy import destroy


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def entry():
    private_dir.ensure_private_dir_exists(settings.APP_NAME)


entry.add_command(create)
entry.add_command(destroy)
