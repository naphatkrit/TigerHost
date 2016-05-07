import click
import subprocess32 as subprocess

from click_extensions import echo_heading
from click_extensions.decorators import print_markers

from deploy import settings
from deploy.secret import store
from deploy.utils import path_utils
from deploy.utils.decorators import ensure_deiscli_exists, skip_if_debug
from deploy.utils.utils import random_string


@click.command('create-admin')
@click.option('--password', '-p', default=None, help='The password of the admin user. By default, create a random password.')
@click.option('--email', '-e', required=True, help='The email of the admin user. A good choice is {netid}+deis.admin@princeton.edu, or a non-Princeton email.')
@print_markers
@ensure_deiscli_exists
@skip_if_debug
def create_admin(password, email):
    """Create an admin user on Deis
    """
    echo_heading('Creating admin user.')
    username = 'admin'
    if password is None:
        password = random_string(length=30)
    deis = path_utils.executable_path('deis')
    subprocess.check_call([deis, 'register',
                           'http://deis.' + settings.DOMAIN_NAME,
                           '--username={}'.format(username), '--email={}'.format(email), '--password={}'.format(password)])
    store.set('deis__username', username)
    store.set('deis__password', password)
    store.set('deis__email', email)
    click.echo('Done.')
