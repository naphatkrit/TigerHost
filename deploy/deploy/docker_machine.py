import os
import shutil
import subprocess32 as subprocess

from deploy.secret.exceptions import SecretNotFoundError
from deploy.secret.secret_dir import secret_dir_path


def docker_machine_storage_path():
    return os.path.join(secret_dir_path(), 'docker_machine')


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

    @type machine_name: str
    @type target_directory: str

    @raises: SecretNotFoundError
    """
    dir_path = os.path.join(docker_machine_storage_path(), 'machines', machine_name)
    if not os.path.exists(dir_path):
        raise SecretNotFoundError
    for f in ['ca.pem', 'cert.pem', 'key.pem']:
        src = os.path.join(dir_path, f)
        dst = os.path.join(target_directory, f)
        shutil.copy2(src, dst)
