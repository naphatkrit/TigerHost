import boto3
import click
import subprocess32 as subprocess

from tigerhost.utils.decorators import print_markers
from tigerhost.utils.click_utils import echo_with_markers

from deploy import settings
from deploy.utils import click_utils
from deploy.utils.decorators import ensure_project_path, require_docker_machine
from deploy.utils.utils import parse_shell_for_exports, random_string


def _get_secret():
    click.echo('Django needs a secret key.')
    choice = click_utils.prompt_choices([
        'Generate a random secret key.',
        'Enter a secret key.'
    ])
    if choice == 0:
        secret = random_string(length=100)
        click.echo('Generated secret.')
    else:
        # TODO only accept [a-zA-Z0-9]
        secret = click.prompt('Secret', type=str, confirmation_prompt=True)
    return secret


@click.command()
@click.option('--elastic-ip-id', '-e', default=None, help='Elastic IP allocation ID, used to associate the created machine with. Creates a new Elastic IP if not provided.')
@click.option('--email', '-e', required=True, help='The email of the Deis admin user. A good choice is {netid}+deis.admin@princeton.edu, or a non-Princeton email.')
@click.option('--hosted-zone-id', '-h', required=True, help='Route 53 Hosted Zone ID for {}'.format(settings.DOMAIN_NAME))
@click.option('--rds-database/--no-rds-database', default=False, help='Control whether TigerHost uses a dedicated RDS database, or use one on the addon.')
@click.option('--secret', '-s', default=None, help='Django secret key.')
@print_markers
@ensure_project_path
@require_docker_machine
def create(elastic_ip_id, email, rds_database, secret, hosted_zone_id):
    if secret is None:
        secret = _get_secret()
    if elastic_ip_id is None:
        if not settings.DEBUG:
            echo_with_markers('Allocating a new Elastic IP.', marker='-')
            client = boto3.client('ec2')
            elastic_ip_id = client.allocate_address(Domain='vpc')['AllocationId']
            click.echo('Done. Allocation ID: {}'.format(elastic_ip_id))
        else:
            # not used anyways
            elastic_ip_id = 'dummy-ip-id'
    subprocess.check_call([settings.APP_NAME, 'deis', 'create'])
    subprocess.check_call([settings.APP_NAME, 'deis', 'configure-dns', '--hosted-zone-id', hosted_zone_id])

    database_url = None
    addons_ip = None

    if rds_database:
        # TODO implement this
        click.abort()
    else:
        db_container_name = random_string(length=50)
        subprocess.check_call(
            [settings.APP_NAME, 'addons', 'create', '--database', db_container_name])
        addons_ip = subprocess.check_output(
            ['docker-machine', 'ip', 'tigerhost-addons-aws']).strip()
        database_url = 'postgres://{name}@{ip}:5432/{name}'.format(
            name=db_container_name,
            ip=addons_ip,
        )

    subprocess.check_call([settings.APP_NAME, 'addons', 'copy-credentials'])

    env_text = subprocess.check_output(
        ['docker-machine', 'env', 'tigerhost-addons-aws'])
    env = parse_shell_for_exports(env_text)
    subprocess.check_call(
        [settings.APP_NAME, 'main', 'create',
         '--addon-docker-host', env['DOCKER_HOST'],
         '--database', database_url,
         '--elastic-ip-id', elastic_ip_id,
         '--secret', secret,
         ])

    subprocess.check_call([settings.APP_NAME, 'main', 'configure-dns', '--elastic-ip-id', elastic_ip_id, '--hosted-zone-id', hosted_zone_id])

    subprocess.check_call([settings.APP_NAME, 'deis', 'create-admin', '--email', email])
