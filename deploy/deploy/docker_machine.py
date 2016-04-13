import os
import shutil
import subprocess32 as subprocess

from deploy.secret.secret_dir import secret_dir_path
from deploy.utils.utils import parse_shell_for_exports


class MachineNotFoundError(Exception):
    pass


def docker_machine_storage_path():
    """Return the special storage path for docker-machine.

    docker-machine typically uses ~/.docker/machine as
    the storage path, but that is not portable. We want to be
    able to keep track of which machines have been the deployed,
    and the best way to do that is in the secret directory

    :rtype: str
    """
    return os.path.join(secret_dir_path(), 'docker_machine')


def _machine_path(machine_name):
    return os.path.join(docker_machine_storage_path(), 'machines', machine_name)


def _process_arguments(cmd, *args, **kwargs):
    cmd = ['docker-machine', '--storage-path',
           docker_machine_storage_path()] + cmd
    return [cmd] + list(args), kwargs


def check_call(cmd, *args, **kwargs):
    """This is like subprocess.check_call, except cmd is prefixed with
    docker-machine --storage-path STORAGE_PATH
    """
    args, kwargs = _process_arguments(cmd, *args, **kwargs)
    return subprocess.check_call(*args, **kwargs)


def check_output(cmd, *args, **kwargs):
    """This is like subprocess.check_output, except cmd is prefixed with
    docker-machine --storage-path STORAGE_PATH
    """
    args, kwargs = _process_arguments(cmd, *args, **kwargs)
    return subprocess.check_output(*args, **kwargs)


def retrieve_credentials(machine_name, target_directory):
    """Given a docker machine, retrieve the credentials
    stored and copy it to the target directory.

    :param str machine_name:
    :param str target_directory:

    :raises deploy.docker_machine.MachineNotFoundError:
    """
    dir_path = _machine_path(machine_name)
    if not os.path.exists(dir_path):
        raise MachineNotFoundError
    for f in ['ca.pem', 'cert.pem', 'key.pem']:
        src = os.path.join(dir_path, f)
        dst = os.path.join(target_directory, f)
        shutil.copy2(src, dst)


def get_url(machine_name):
    """Given a docker machine, retrieve the URL for this machine.
    This is the DOCKER_HOST env variable from running
    `docker-machine env {name}`

    :param str machine_name: the name of the docker machine

    :rtype: str
    :returns: machine URL
    """
    dir_path = _machine_path(machine_name)
    if not os.path.exists(dir_path):
        raise MachineNotFoundError

    env_text = check_output(
        ['env', machine_name])
    env = parse_shell_for_exports(env_text)
    return env['DOCKER_HOST']
