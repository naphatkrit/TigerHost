import click
import os
import shutil

from functools import update_wrapper
from tigerhost import exit_codes

from tigerhostctl.project import get_project_path, save_project_path, default_project_path, clone_project
from tigerhostctl.utils import click_utils, path_utils


def ensure_project_path(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        """
        @type ctx: click.Context
        """
        if get_project_path() is None:
            click.echo('Config project_path not set.')
            click.echo('You can do one of the following:')
            choice = click_utils.prompt_choices([
                'Clone the repository to {}.'.format(default_project_path()),
                'Specify the path to an existing repo.'
            ])
            if choice == 0:
                path = default_project_path()
                if os.path.exists(path):
                    click.confirm('Path {} already exists. Continuing will remove this path.'.format(path), default=True, abort=True)
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                click.echo('Cloning to {}...'.format(path), nl=False)
                clone_project()
                click.secho('Done', fg='black', bg='green')
                save_project_path(path)
            else:
                value = click.prompt(
                    'Please enter the path to your project', type=str)
                value = path_utils.canonical_path(value)
                if not os.path.exists(value) or not os.path.isdir(value):
                    click.echo('This directory does not exist.')
                    ctx.exit(code=exit_codes.OTHER_FAILURE)
                click.confirm('Is your project at {}?'.format(
                    value), default=True, abort=True)
                save_project_path(value)
        return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(new_func, f)
