import os

_private_dir_name = '.tigerhost'


class PrivateDirConflictError(Exception):
    pass


_private_dir_path = os.path.expanduser(os.path.join('~', _private_dir_name))


def private_dir_path():
    return _private_dir_path


def ensure_private_dir_exists():
    """Ensures that the private directory exists and is a directory.
    """
    path = private_dir_path()
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        if not os.path.isdir(path):
            raise PrivateDirConflictError
