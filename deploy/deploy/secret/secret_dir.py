import os

from click_extensions import private_dir

from deploy import settings
from deploy.utils import path_utils


class SecretDirConflictError(Exception):
    pass


def secret_dir_path():
    """Returns the path to the secret directory.

    :rtype: str
    :returns: path
    """
    return path_utils.canonical_path(os.path.join(private_dir.private_dir_path(settings.APP_NAME), 'secret'))


def ensure_secret_dir_exists():
    """Ensures that the secret directory exists and is a directory.
    """
    path = secret_dir_path()
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        if not os.path.isdir(path):
            raise SecretDirConflictError
