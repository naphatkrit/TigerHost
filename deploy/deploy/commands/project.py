import click
import os
import shutil

from click_extensions import decorators

from deploy.project import clone_project, default_project_path, save_project_path
from deploy.utils import path_utils


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group()
def project(context_settings=CONTEXT_SETTINGS):
    """This is a group of commands for managing the TigerHost project path.
    """
    pass


@project.command('set-path')
@click.argument('path', type=click.Path(exists=True))
@decorators.print_markers
def set_path(path):
    """Set the project path.
    """
    path = path_utils.canonical_path(path)
    save_project_path(path)
    click.echo('Set project path to {}.'.format(path))


@project.command()
@click.option('--force', '-f', is_flag=True, help='Force the clone, deleting anything at the private path if it exists.')
@decorators.print_markers
def clone(force):
    """Clone a copy of the TigerHost project to
    a private location and set the project path
    to the cloned location.
    """
    path = default_project_path()
    if os.path.exists(path):
        if not force:
            click.confirm('Path {} already exists. Continuing will remove this path.'.format(
                path), default=True, abort=True)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    click.echo('Cloning to {}...'.format(path), nl=False)
    clone_project()
    click.secho('Done', fg='black', bg='green')
    save_project_path(path)
