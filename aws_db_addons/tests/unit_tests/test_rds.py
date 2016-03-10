import mock
import pytest

from aws_db_addons import rds


@pytest.mark.django_db
def test_create_instance(db_instance):
    mock_client = mock.MagicMock()
    with mock.patch('aws_db_addons.rds.boto3.client') as mocked:
        mocked.return_value = mock_client
        rds.create_instance(db_instance, 'postgres')
    assert mock_client.create_db_instance.call_count == 1
    _, kwargs = mock_client.create_db_instance.call_args
    assert kwargs['DBInstanceIdentifier'] == db_instance.aws_instance_identifier
    assert kwargs['DBName'] == db_instance.db_name
    assert kwargs['MasterUsername'] == db_instance.master_username
    assert kwargs['MasterUserPassword'] == db_instance.master_password
    assert kwargs['Engine'] == 'postgres'


@pytest.mark.django_db
def get_endpoint_simple(db_instance):
    mock_client = mock.MagicMock()
    mock_client.describe_db_instances.return_value = {
        'DBInstances': [{
            'DBInstanceStatus': 'available',
            'Endpoint': {
                'Address': 'localhost',
                'Port': 1234
            }
        }]
    }
    with mock.patch('aws_db_addons.rds.boto3.client') as mocked:
        mocked.return_value = mock_client
        endpoint = rds.get_endpoint(db_instance)
    assert endpoint == 'localhost:1234'
    mock_client.describe_db_instances.assert_called_once_with(DDBInstanceIdentifier=db_instance.aws_instance_identifier)


@pytest.mark.django_db
def get_endpoint_not_ready(db_instance):
    mock_client = mock.MagicMock()
    mock_client.describe_db_instances.return_value = {
        'DBInstances': [{
            'DBInstanceStatus': 'creating',
            'Endpoint': {
                'Address': 'localhost',
                'Port': 1234
            }
        }]
    }
    with mock.patch('aws_db_addons.rds.boto3.client') as mocked:
        mocked.return_value = mock_client
        with pytest.raises(rds.RdsNotReadyError):
            rds.get_endpoint(db_instance)
    mock_client.describe_db_instances.assert_called_once_with(DDBInstanceIdentifier=db_instance.aws_instance_identifier)


@pytest.mark.django_db
def test_delete_instance(db_instance):
    mock_client = mock.MagicMock()
    with mock.patch('aws_db_addons.rds.boto3.client') as mocked:
        mocked.return_value = mock_client
        rds.delete_instance(db_instance)
    assert mock_client.delete_db_instance.call_count == 1
    _, kwargs = mock_client.delete_db_instance.call_args
    assert kwargs['DBInstanceIdentifier'] == db_instance.aws_instance_identifier
