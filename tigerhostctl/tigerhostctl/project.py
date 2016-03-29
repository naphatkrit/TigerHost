from tigerhostctl import user_config
from tigerhostctl.utils import utils


_project_path_key = 'project_path'


def get_project_path():
    """Get the TigerHost project path,
    returning None if it is not stored

    @rtype: str
    """
    return user_config.get(_project_path_key)


def save_project_path(path):
    """Save the path in its canonical form.
    """
    user_config.set(_project_path_key, utils.canonical_path(path))
