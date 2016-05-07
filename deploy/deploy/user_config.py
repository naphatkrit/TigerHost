import json
import os

from click_extensions import private_dir

from deploy import settings


def _config_path():
    return os.path.join(private_dir.private_dir_path(settings.APP_NAME), 'config.json')


def _get_config_dict():
    """Get the user config file parsed as a dictionary.

    :rtype: dict
    """
    path = _config_path()
    if not os.path.exists(path):
        return dict()
    with open(path, 'r') as f:
        config = json.load(f)
    assert isinstance(config, dict)
    return config


def _save_config_dict(config_dict):
    path = _config_path()
    with open(path, 'w') as f:
        json.dump(config_dict, f, sort_keys=True, indent=4, separators=(',', ': '))


def get(key, default=None):
    """Try to get user config `key`, returning default if not found.

    :type: str
    """
    config = _get_config_dict()
    return config.get(key, default)


def set(key, value):
    """Save the user config
    :param str key:
    :param (str | dict | list | int | float | bool) value:
    """
    # TODO this should be implemented with a lock
    config = _get_config_dict()
    config[key] = value
    _save_config_dict(config)
