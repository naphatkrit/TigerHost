import boto3
import click

from click_extensions import echo_heading
from click_extensions.decorators import print_markers

from deploy import settings
from deploy.utils.decorators import option_hosted_zone_id, skip_if_debug


@click.command('configure-dns')
@click.option('--elastic-ip-id', '-e', required=True, help='Elastic IP allocation ID')
@print_markers
@option_hosted_zone_id
@skip_if_debug
def configure_dns(elastic_ip_id, hosted_zone_id):
    """Configure the DNS of the main TigerHost server.

    This points tigerhost.com (not a subdomain) to the main server
    """
    echo_heading('Creating A record.', marker='-', marker_color='magenta')
    ec2 = boto3.resource('ec2')
    client = boto3.client('route53')
    client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Comment': 'Test comment',
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': settings.DOMAIN_NAME,
                        'Type': 'A',
                        'TTL': 60,
                        'ResourceRecords': [
                            {
                                'Value': ec2.VpcAddress(elastic_ip_id).public_ip
                            },
                        ],
                    }
                },
            ]
        }
    )
    click.echo('Done.')
