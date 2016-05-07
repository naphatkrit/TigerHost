import os

from click_extensions import private_dir
from tigerhost.vcs.git import GitVcs

from deploy import settings, user_config
from deploy.utils import path_utils


_project_path_key = 'project_path'


def default_project_path():
    """The default project path
    """
    return os.path.join(private_dir.private_dir_path(settings.APP_NAME), 'project')


def get_project_path():
    """Get the TigerHost project path,
    returning None if it is not stored

    :rtype: str
    """
    return user_config.get(_project_path_key)


def save_project_path(path):
    """Save the path in its canonical form.
    """
    user_config.set(_project_path_key, path_utils.canonical_path(path))


def clone_project():
    """Clone a copy of the repo to the default project path
    """
    GitVcs.clone(settings.PROJECT_REMOTE, default_project_path())
