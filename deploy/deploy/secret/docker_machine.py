import os
import shutil
import subprocess32 as subprocess

from deploy.secret.exceptions import SecretNotFoundError
from deploy.secret.secret_dir import secret_dir_path
from deploy.utils.utils import parse_shell_for_exports


def store_credentials(machine_name):
    """Given a docker machine, save the credentials
    needed for the docker client.

    @type machine_name: str
    """
    dir_path = os.path.join(secret_dir_path(), 'docker_machines', machine_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    env_text = subprocess.check_output(['docker-machine', 'env', machine_name])
    env = parse_shell_for_exports(env_text)
    cert_path = env['DOCKER_CERT_PATH']
    for f in ['ca.pem', 'cert.pem', 'key.pem']:
        src = os.path.join(cert_path, f)
        dst = os.path.join(dir_path, f)
        shutil.copy2(src, dst)


def retrieve_credentials(machine_name, target_directory):
    """Given a docker machine, retrieve the credentials
    stored and copy it to the target directory.

    @type machine_name: str
    @type target_directory: str

    @raises: SecretNotFoundError
    """
    dir_path = os.path.join(secret_dir_path(), 'docker_machines', machine_name)
    if not os.path.exists(dir_path):
        raise SecretNotFoundError
    for f in ['ca.pem', 'cert.pem', 'key.pem']:
        src = os.path.join(dir_path, f)
        dst = os.path.join(target_directory, f)
        shutil.copy2(src, dst)


def remove_credentials(machine_name):
    """Remove any credentials stored for this machine.
    If not found, nothing happens.

    @type machine_name: str
    """
    dir_path = os.path.join(secret_dir_path(), 'docker_machines', machine_name)
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
