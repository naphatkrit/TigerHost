import click

import tigerhost


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=tigerhost.__version__, prog_name='TigerHost')
def entry():
    pass
