import click

import tigerhostctl


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=tigerhostctl.__version__, prog_name='TigerHostCtl')
def entry():
    pass
