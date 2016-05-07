import os

from click_extensions import private_dir

from deploy import settings


def canonical_path(path):
    """Return the canonical path. This expands ~ and resolves
    any symbolic links, and returns the absolute path.

    :param str path:

    :rtype: str
    """
    return os.path.realpath(os.path.expanduser(path))


def executable_path(name):
    """Return the canonical path to a private executable file

    :param str name:

    :rtype: str
    """
    return canonical_path(os.path.join(private_dir.private_dir_path(settings.APP_NAME), name))


def ssh_path(name):
    """Return the canonical path to ~/.ssh/{name}

    :rtype: str
    """
    return canonical_path(os.path.join('~/.ssh', name))


def docker_machine_path(machine_name):
    from deploy.docker_machine import docker_machine_storage_path
    return canonical_path(os.path.join(docker_machine_storage_path(), 'machines', machine_name))
