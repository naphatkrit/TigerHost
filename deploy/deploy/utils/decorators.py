import boto3
import botocore
import click
import os
import shutil
import stat

from functools import update_wrapper
from tigerhost import exit_codes

from deploy.project import get_project_path, save_project_path, default_project_path, clone_project
from deploy.utils import click_utils, path_utils


def ensure_project_path(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        """
        @type ctx: click.Context
        """
        if get_project_path() is None:
            click.echo('Config project_path not set.')
            click.echo('You can do one of the following:')
            choice = click_utils.prompt_choices([
                'Clone the repository to {}.'.format(default_project_path()),
                'Specify the path to an existing repo.'
            ])
            if choice == 0:
                path = default_project_path()
                if os.path.exists(path):
                    click.confirm('Path {} already exists. Continuing will remove this path.'.format(
                        path), default=True, abort=True)
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                click.echo('Cloning to {}...'.format(path), nl=False)
                clone_project()
                click.secho('Done', fg='black', bg='green')
                save_project_path(path)
            else:
                value = click.prompt(
                    'Please enter the path to your project', type=str)
                value = path_utils.canonical_path(value)
                if not os.path.exists(value) or not os.path.isdir(value):
                    click.echo('This directory does not exist.')
                    ctx.exit(code=exit_codes.OTHER_FAILURE)
                click.confirm('Is your project at {}?'.format(
                    value), default=True, abort=True)
                save_project_path(value)
        return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(new_func, f)


def _ssh_path(name):
    return os.path.join('~/.ssh', name)


def ensure_key_pair(name):
    """Ensures that a key pair with the name `name` exists,
    both on AWS and in `~/.ssh/{name}`
    """
    def decorator(old_func):
        @click.pass_context
        def new_func(ctx, *args, **kwargs):
            ec2 = boto3.resource('ec2')
            key_path = os.path.expanduser(_ssh_path(name))
            exists_on_aws = True
            key_pair = ec2.KeyPair(name)
            try:
                key_pair.key_fingerprint
            except botocore.exceptions.ClientError:
                exists_on_aws = False
            if not os.path.exists(key_path) or (not exists_on_aws and not os.path.exists(key_path + '.pub')):
                if not os.path.exists(key_path):
                    click.echo(
                        'Key pair does not exist at {}.'.format(key_path))
                else:
                    click.echo('Key does not exist at {}.pub.'.format(key_path))
                click.confirm('Create a new key on AWS and save it?',
                              default=True, abort=True)
                key_pair.delete()
                client = boto3.client('ec2')
                key_info = client.create_key_pair(KeyName=name)
                with open(key_path, 'w') as f:
                    f.write(key_info['KeyMaterial'])
                os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)
            else:
                # key exists, make sure key also exists on AWS
                if not exists_on_aws:
                    click.echo('Key exists locally, but not on AWS.')
                    click.confirm('Import key at {} to AWS?'.format(
                        key_path), default=True, abort=True)
                    with open(key_path + '.pub', 'r') as f:
                        public_key = f.read()
                    client = boto3.client('ec2')
                    client.import_key_pair(
                        KeyName=name,
                        PublicKeyMaterial=public_key,
                    )
                # TODO should verify fingerprint with public key
            return ctx.invoke(old_func, *args, **kwargs)
        return update_wrapper(new_func, old_func)
    return decorator
