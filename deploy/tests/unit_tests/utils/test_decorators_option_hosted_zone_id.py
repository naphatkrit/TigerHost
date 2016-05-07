import click
import mock
import pytest

from click_extensions import exit_codes

from deploy import settings
from deploy.utils.decorators import option_hosted_zone_id


@click.command()
@option_hosted_zone_id
def dummy(hosted_zone_id):
    click.echo(hosted_zone_id)


@pytest.fixture(scope='function')
def fake_route53_client():
    mocked = mock.Mock()
    mocked.list_hosted_zones_by_name = mock.Mock()
    return mocked


def test_option_hosted_zone_id_success(runner, fake_route53_client):
    fake_route53_client.list_hosted_zones_by_name.return_value = {
        'HostedZones': [
            {
                'Id': '/hostedzones/12345',
            }
        ]
    }
    with mock.patch('boto3.client') as mocked:
        mocked.return_value = fake_route53_client
        result = runner.invoke(dummy)
    assert result.exit_code == exit_codes.SUCCESS
    assert '12345' == result.output.split('\n')[-2]
    fake_route53_client.list_hosted_zones_by_name.assert_called_once_with(
        DNSName=settings.DOMAIN_NAME)


def test_option_hosted_zone_id_failure_none(runner, fake_route53_client):
    fake_route53_client.list_hosted_zones_by_name.return_value = {
        'HostedZones': [
        ]
    }
    with mock.patch('boto3.client') as mocked:
        mocked.return_value = fake_route53_client
        result = runner.invoke(dummy)
    assert result.exit_code == exit_codes.OTHER_FAILURE
    fake_route53_client.list_hosted_zones_by_name.assert_called_once_with(
        DNSName=settings.DOMAIN_NAME)


def test_option_hosted_zone_id_failure_many(runner, fake_route53_client):
    fake_route53_client.list_hosted_zones_by_name.return_value = {
        'HostedZones': [
            {
                'Id': '/hostedzones/12345',
            },
            {
                'Id': '/hostedzones/123456',
            }
        ]
    }
    with mock.patch('boto3.client') as mocked:
        mocked.return_value = fake_route53_client
        result = runner.invoke(dummy)
    assert result.exit_code == exit_codes.OTHER_FAILURE
    fake_route53_client.list_hosted_zones_by_name.assert_called_once_with(
        DNSName=settings.DOMAIN_NAME)


def test_option_hosted_zone_id_explicit(runner):
    result = runner.invoke(dummy, ['--hosted-zone-id', '12345'])
    assert result.exit_code == exit_codes.SUCCESS
    assert '12345' == result.output.split('\n')[-2]
