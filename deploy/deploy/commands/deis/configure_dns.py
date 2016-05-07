import boto3
import click

from click_extensions import echo_heading
from click_extensions.decorators import print_markers

from deploy import settings
from deploy.utils.decorators import option_hosted_zone_id, skip_if_debug


@click.command('configure-dns')
@click.option('--stack', '-s', default='deis', help='The name of the cloud formation stack.')
@print_markers
@option_hosted_zone_id
@skip_if_debug
def configure_dns(stack, hosted_zone_id):
    """Configure the DNS of the Deis cluster.

    This points *.tigerhostapp.com to Deis.
    """
    echo_heading('Creating A record.', marker='-', marker_color='magenta')
    cloudformation = boto3.resource('cloudformation')
    stack_instance = cloudformation.Stack(stack)

    dns_name = None
    for x in stack_instance.outputs:
        if x['OutputKey'] == 'DNSName':
            dns_name = x['OutputValue']
    assert dns_name is not None

    # TODO this fails on accounts with more than 400 load balancers
    elb_hosted_zone_id = None
    elb_client = boto3.client('elb')
    for x in elb_client.describe_load_balancers()['LoadBalancerDescriptions']:
        if x['DNSName'] == dns_name:
            elb_hosted_zone_id = x['CanonicalHostedZoneNameID']
    assert elb_hosted_zone_id is not None

    client = boto3.client('route53')
    client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Comment': 'Test comment',
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': '*.' + settings.DOMAIN_NAME,
                        'Type': 'A',
                        'AliasTarget': {
                            'HostedZoneId': elb_hosted_zone_id,
                            'DNSName': dns_name,
                            'EvaluateTargetHealth': False
                        },
                    }
                },
            ]
        }
    )
    click.echo('Done.')
