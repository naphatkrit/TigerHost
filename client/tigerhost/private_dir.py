import os

_private_dir_name = '.tigerhost'


class PrivateDirConflictError(Exception):
    pass


private_dir_path = os.path.normpath(os.path.join('~', _private_dir_name))


def ensure_private_dir_exists():
    """Ensures that the private directory exists and is a directory.
    """
    path = private_dir_path
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        if not os.path.isdir(path):
            raise PrivateDirConflictError
