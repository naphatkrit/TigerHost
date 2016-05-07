import click
import os
import shutil

from click_extensions.decorators import print_markers
from tigerhost.vcs.git import GitVcs

from deploy.secret import secret_dir


@click.command('secret-clone')
@click.argument('remote_url')
@click.option('--force', '-f', default=False, is_flag=True, help='If a secret directory already exists, remove it.')
@print_markers
def secret_clone(remote_url, force):
    """Clone a repo from the remote URL as the secret directory.
    """
    path = secret_dir.secret_dir_path()
    if os.path.exists(path):
        if not force:
            click.echo(
                'Secret directory at {} already exists. This may mean that you have already deployed an instance of TigerHost.'.format(path))
            click.confirm(
                'Remove existing secret directory? You will no longer be able to manage any previously deployed instances of TigerHost.', default=False, abort=True)
        shutil.rmtree(path)
    GitVcs.clone(remote_url, path)
