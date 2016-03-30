import click

from tigerhost import private_dir

import tigerhostctl

from tigerhostctl import settings


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=tigerhostctl.__version__, prog_name='TigerHostCtl')
def entry():
    private_dir.ensure_private_dir_exists(settings.APP_NAME)
