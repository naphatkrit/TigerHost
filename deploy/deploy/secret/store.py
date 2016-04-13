"""A Key-Value store model for secrets.

Internally, each key-value pair is stored as a file,
with the name of the file being the key. Therefore,
key-comparison is case insensitive.
"""
import json
import os

from deploy.secret.secret_dir import secret_dir_path


def _store_base_dir():
    return os.path.join(secret_dir_path(), 'store')


def get(key, default=None):
    """Try to get the secret stored under `key`, returning
    default if not found.

    :param str key:

    :rtype: (str | dict | list | int | float | bool)
    :returns: the value stored, or default
    """
    path = os.path.join(_store_base_dir(), key.lower())
    if not os.path.exists(path):
        return default
    with open(path, 'r') as f:
        return json.load(f)


def set(key, value):
    """Save the key-value pair.

    :param str key:
    :param value:
    :type value: (str | dict | list | int | float | bool)
    """
    base = _store_base_dir()
    if not os.path.exists(base):
        os.mkdir(base)
    path = os.path.join(base, key.lower())
    with open(path, 'w') as f:
        json.dump(value, f)


def unset(key):
    """Unset the key-value pair. Does nothing if not found.

    :param str key:
    """
    path = os.path.join(_store_base_dir(), key.lower())
    if os.path.exists(path):
        os.remove(path)
