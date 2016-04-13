"""A module to manage app private directory (~/.app_name)"""
import click
import os


class PrivateDirConflictError(Exception):
    """When a file whose name is the same as the private directory
    exists
    """
    pass


def private_dir_path(app_name):
    """Returns the private directory path

    :param str app_name: the name of the app

    :rtype: str
    :returns: directory path
    """
    _private_dir_path = os.path.expanduser(click.get_app_dir(
        app_name,
        force_posix=True,  # forces to ~/.tigerhost on Mac and Unix
    ))
    return _private_dir_path


def ensure_private_dir_exists(app_name):
    """Ensures that the private directory exists and is a directory.

    :param str app_name: the name of the app
    """
    path = private_dir_path(app_name)
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        if not os.path.isdir(path):
            raise PrivateDirConflictError
