import boto3
import botocore
import click
import os
import requests
import shutil
import stat
import subprocess32 as subprocess

from functools import update_wrapper
from temp_utils import contextmanagers
from click_extensions import echo_heading, exit_codes, private_dir

from deploy import settings
from deploy.project import get_project_path, save_project_path, default_project_path, clone_project
from deploy.utils import click_utils, path_utils, utils


def ensure_project_path(f):
    """Ensure that the project path exists. In the event that it
    does not exist, prompt the user to specify the path
    """
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        """
        :param click.Context ctx:
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


def require_executable(executable):
    """Check if an executable is installed. If not, exit with an
    error.
    """
    def decorator(f):
        @click.pass_context
        def new_func(ctx, *args, **kwargs):
            """
            :param click.Context ctx:
            """
            if utils.which(executable) is None:
                click.echo('{} is not installed. Please install it.'.format(executable))
                ctx.exit(code=exit_codes.OTHER_FAILURE)
            return ctx.invoke(f, *args, **kwargs)
        return update_wrapper(new_func, f)
    return decorator


require_docker_machine = require_executable('docker-machine')
require_docker_compose = require_executable('docker-compose')


def option_hosted_zone_id(f):
    """Similar to click.option for hosted-zone-id, but in the event
    that the user does not specify the option, try to retrieve
    the ID from AWS and only error out if that fails or is ambiguous.
    """
    @click.option('--hosted-zone-id', '-hz', default=None, help='Route 53 Hosted Zone ID for {}'.format(settings.DOMAIN_NAME))
    @click.pass_context
    def new_func(ctx, hosted_zone_id, *args, **kwargs):
        """
        :param click.Context ctx:
        """
        if hosted_zone_id is None:
            echo_heading('Trying to find hosted zone for {}.'.format(settings.DOMAIN_NAME), marker='-', marker_color='magenta')
            client = boto3.client('route53')
            response = client.list_hosted_zones_by_name(
                DNSName=settings.DOMAIN_NAME
            )
            if len(response['HostedZones']) == 0:
                click.echo('Unable to find a Hosted Zone for {}. Please specify it explicitly by passing --hosted-zone-id/-hz.')
                ctx.exit(code=exit_codes.OTHER_FAILURE)
            elif len(response['HostedZones']) > 1:
                click.echo('Found multiple Hosted Zones for {}. Please specify one explicitly by passing --hosted-zone-id/-hz.')
                ctx.exit(code=exit_codes.OTHER_FAILURE)
            hosted_zone_id = response['HostedZones'][0]['Id'].split('/')[-1]
            click.echo('Done.')
        return ctx.invoke(f, hosted_zone_id=hosted_zone_id, *args, **kwargs)
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
                    click.echo(
                        'Key does not exist at {}.pub.'.format(key_path))
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


def skip_if_debug(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        """
        :param click.Context ctx:
        """
        if settings.DEBUG:
            click.echo('Skipping because DEBUG is True.')
            ctx.exit()
        return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(new_func, f)


def ensure_executable_exists(name, get_executable):
    """Ensures that the private executable exists. If it doesn't, then
    call get_executable, which must be a callable that installs
    the executable.
    """
    def decorator(f):
        @click.pass_context
        def new_func(ctx, *args, **kwargs):
            """
            @type ctx: click.Context
            """
            path = path_utils.executable_path(name)
            if not os.path.exists(path):
                echo_heading('Installing {}.'.format(name), marker='-', marker_color='magenta')
                get_executable()
                assert os.path.exists(path)
            return ctx.invoke(f, *args, **kwargs)
        return update_wrapper(new_func, f)
    return decorator


def _install_deisctl():
    script = requests.get(settings.DEISCTL_INSTALL_URL).text
    subprocess.check_call(['bash', '-c', script, 'install.sh',
                           '1.12.3', private_dir.private_dir_path(settings.APP_NAME)])
    os.chmod(path_utils.executable_path('deisctl'), stat.S_IRWXU)


def _install_deis():
    script = requests.get(settings.DEIS_INSTALL_URL).text
    with contextmanagers.chdir(private_dir.private_dir_path(settings.APP_NAME)):
        subprocess.check_call(['bash', '-c', script, 'install.sh', '1.12.3'])
    os.chmod(path_utils.executable_path('deis'), stat.S_IRWXU)


ensure_deisctl_exists = ensure_executable_exists('deisctl', _install_deisctl)
ensure_deiscli_exists = ensure_executable_exists('deis', _install_deis)
