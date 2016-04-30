import botocore
import mock
import pytest
import uuid

from api_server.addons.providers.exceptions import AddonProviderError
from aws_db_addons import rds
from aws_db_addons.models import DbInstance
from aws_db_addons.providers.rds_provider import RdsAddonProvider


@pytest.fixture(scope='function')
def provider():
    return RdsAddonProvider(engine='test_engine')


@pytest.fixture(scope='function')
def mock_rds():
    mocked = mock.Mock(spec=rds)
    mocked.RdsNotReadyError = rds.RdsNotReadyError
    return mocked


class MockClientError(botocore.exceptions.ClientError):

    def __init__(self):
        pass


@pytest.mark.django_db
def test_begin_provision_success(provider, mock_rds):
    with mock.patch('aws_db_addons.providers.rds_provider.rds', new=mock_rds):
        result = provider.begin_provision(None)
    assert 'message' in result
    instance = DbInstance.objects.get(uuid=result['uuid'])
    mock_rds.create_instance.assert_called_once_with(instance, provider.engine)


@pytest.mark.django_db
def test_begin_provision_failure(provider, mock_rds):
    mock_rds.create_instance.side_effect = MockClientError
    with mock.patch('aws_db_addons.providers.rds_provider.rds', new=mock_rds):
        with pytest.raises(AddonProviderError):
            provider.begin_provision(None)


@pytest.mark.django_db
def test_provision_complete_success_true(provider, mock_rds, db_instance):
    mock_rds.get_endpoint.return_value = 'localhost:1234'
    with mock.patch('aws_db_addons.providers.rds_provider.rds', new=mock_rds):
        done, _ = provider.provision_complete(db_instance.uuid)
    assert done
    mock_rds.get_endpoint.assert_called_once_with(db_instance)


@pytest.mark.django_db
def test_provision_complete_success_false(provider, mock_rds, db_instance):
    mock_rds.get_endpoint.side_effect = rds.RdsNotReadyError
    with mock.patch('aws_db_addons.providers.rds_provider.rds', new=mock_rds):
        done, seconds = provider.provision_complete(db_instance.uuid)
    assert not done
    assert seconds > 0
    mock_rds.get_endpoint.assert_called_once_with(db_instance)


@pytest.mark.django_db
def test_provision_complete_failure_does_not_exist(provider, mock_rds):
    with mock.patch('aws_db_addons.providers.rds_provider.rds', new=mock_rds):
        with pytest.raises(AddonProviderError):
            provider.provision_complete(uuid.uuid4())


@pytest.mark.django_db
def test_provision_complete_failure_client(provider, mock_rds, db_instance):
    mock_rds.get_endpoint.side_effect = MockClientError
    with mock.patch('aws_db_addons.providers.rds_provider.rds', new=mock_rds):
        with pytest.raises(AddonProviderError):
            provider.provision_complete(db_instance.uuid)
    mock_rds.get_endpoint.assert_called_once_with(db_instance)


@pytest.mark.django_db
def test_get_config_success(provider, mock_rds, db_instance):
    mock_rds.get_endpoint.return_value = 'localhost:1234'
    with mock.patch('aws_db_addons.providers.rds_provider.rds', new=mock_rds):
        result = provider.get_config(db_instance.uuid)
    mock_rds.get_endpoint.assert_called_once_with(db_instance)
    assert 'localhost:1234' in result['config'][provider.config_name]


@pytest.mark.django_db
def test_get_config_success_with_config_customization(provider, mock_rds, db_instance):
    mock_rds.get_endpoint.return_value = 'localhost:1234'
    with mock.patch('aws_db_addons.providers.rds_provider.rds', new=mock_rds):
        result = provider.get_config(
            db_instance.uuid, config_customization='TEST')
    mock_rds.get_endpoint.assert_called_once_with(db_instance)
    assert 'localhost:1234' in result['config'][
        provider._get_config_name('TEST')]


@pytest.mark.django_db
def test_get_config_failure_not_ready(provider, mock_rds, db_instance):
    mock_rds.get_endpoint.side_effect = rds.RdsNotReadyError
    with mock.patch('aws_db_addons.providers.rds_provider.rds', new=mock_rds):
        with pytest.raises(AddonProviderError):
            provider.get_config(db_instance.uuid)
    mock_rds.get_endpoint.assert_called_once_with(db_instance)


@pytest.mark.django_db
def test_get_config_failure_does_not_exist(provider, mock_rds):
    with mock.patch('aws_db_addons.providers.rds_provider.rds', new=mock_rds):
        with pytest.raises(AddonProviderError):
            provider.get_config(uuid.uuid4())


@pytest.mark.django_db
def test_get_config_failure_client(provider, mock_rds, db_instance):
    mock_rds.get_endpoint.side_effect = MockClientError
    with mock.patch('aws_db_addons.providers.rds_provider.rds', new=mock_rds):
        with pytest.raises(AddonProviderError):
            provider.get_config(db_instance.uuid)
    mock_rds.get_endpoint.assert_called_once_with(db_instance)


@pytest.mark.django_db
def test_deprovision_success(provider, mock_rds, db_instance):
    with mock.patch('aws_db_addons.providers.rds_provider.rds', new=mock_rds):
        result = provider.deprovision(db_instance.uuid)
    mock_rds.delete_instance.assert_called_once_with(db_instance)
    assert 'message' in result


@pytest.mark.django_db
def test_deprovision_failure_client(provider, mock_rds, db_instance):
    mock_rds.delete_instance.side_effect = MockClientError
    with mock.patch('aws_db_addons.providers.rds_provider.rds', new=mock_rds):
        with pytest.raises(AddonProviderError):
            provider.deprovision(db_instance.uuid)
    mock_rds.delete_instance.assert_called_once_with(db_instance)


@pytest.mark.django_db
def test_deprovision_failure_does_not_exist(provider, mock_rds):
    with mock.patch('aws_db_addons.providers.rds_provider.rds', new=mock_rds):
        with pytest.raises(AddonProviderError):
            provider.deprovision(uuid.uuid4())
