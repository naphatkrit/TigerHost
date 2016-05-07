import boto3
import click
import os
import subprocess32 as subprocess

from temp_utils import contextmanagers
from click_extensions.decorators import print_markers

from deploy import settings
from deploy.project import get_project_path
from deploy.utils import path_utils
from deploy.utils.decorators import ensure_project_path, ensure_key_pair, skip_if_debug, ensure_deisctl_exists


@click.command()
@click.option('--stack', '-s', default='deis', help='The name of the cloud formation stack to create.')
@print_markers
@ensure_project_path
@ensure_key_pair('deis')
@ensure_deisctl_exists
@skip_if_debug
def create(stack):
    """Create a new Deis cluster.
    """
    deisctl = path_utils.executable_path('deisctl')
    subprocess.check_call(['ssh-add', path_utils.ssh_path('deis')])
    with contextmanagers.chdir(os.path.join(get_project_path(), 'deis')):
        subprocess.check_call(['make', 'discovery-url'])
        click.echo('Provisioning machines.')
        with contextmanagers.chdir('contrib/aws'):
            subprocess.check_call(['./provision-aws-cluster.sh', stack])
        ec2 = boto3.resource('ec2')
        instances = ec2.instances.filter(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': ['running'],
                },
                {
                    'Name': 'tag:aws:cloudformation:stack-name',
                    'Values': [stack],
                },
            ]
        ).limit(1)
        ip = None
        for i in instances:
            ip = i.public_ip_address
        assert ip is not None
        click.echo('Machines provisioned. An IP address is {}.'.format(ip))
        env = {
            'DEISCTL_TUNNEL': ip
        }
        env.update(os.environ)
        click.echo('Installing Deis.')
        subprocess.check_call([deisctl, 'config', 'platform',
                               'set', 'sshPrivateKey=' + path_utils.ssh_path('deis')], env=env)
        subprocess.check_call(
            [deisctl, 'config', 'platform', 'set', 'domain=' + settings.DOMAIN_NAME], env=env)
        subprocess.check_call([deisctl, 'refresh-units'], env=env)
        subprocess.check_call([deisctl, 'install', 'platform'], env=env)
        subprocess.check_call([deisctl, 'start', 'platform'], env=env)
