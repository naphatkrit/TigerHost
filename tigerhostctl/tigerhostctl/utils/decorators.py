import click
import os

from functools import update_wrapper
from tigerhost import exit_codes

from tigerhostctl.project import get_project_path, save_project_path
from tigerhostctl.utils import path_utils


def ensure_project_path(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        """
        @type ctx: click.Context
        """
        if get_project_path() is None:
            click.echo('Config project_path not set.')
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
