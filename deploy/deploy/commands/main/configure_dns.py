import boto3
import click

from tigerhost.utils.click_utils import echo_with_markers
from tigerhost.utils.decorators import print_markers

from deploy import settings


@click.command('configure-dns')
@click.option('--elastic-ip-id', '-e', required=True, help='Elastic IP allocation ID')
@click.option('--hosted-zone-id', '-h', required=True, help='Route 53 Hosted Zone ID')
@print_markers
def configure_dns(elastic_ip_id, hosted_zone_id):
    echo_with_markers('Creating A record.', marker='-')
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
