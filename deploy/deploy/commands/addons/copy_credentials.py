import click
import os
import shutil
import subprocess32 as subprocess

from tigerhost.utils.decorators import print_markers

from deploy.project import get_project_path
from deploy.utils.decorators import ensure_project_path
from deploy.utils.utils import parse_shell_for_exports


@click.command('copy-credentials')
@click.option('--name', '-n', default='tigerhost-addons-aws', help='The name of the machine. Defaults to tigerhost-addons-aws.')
@print_markers
@ensure_project_path
def copy_credentials(name):
    env_text = subprocess.check_output(['docker-machine', 'env', name])
    env = parse_shell_for_exports(env_text)
    cert_path = env['DOCKER_CERT_PATH']
    project_path = get_project_path()
    target_path = os.path.join(project_path, 'web/credentials')
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    for f in ['ca.pem', 'cert.pem', 'key.pem']:
        src = os.path.join(cert_path, f)
        dst = os.path.join(target_path, f)
        click.echo('Copying {} to {}.'.format(src, dst))
        shutil.copy2(src, dst)
        click.echo()
