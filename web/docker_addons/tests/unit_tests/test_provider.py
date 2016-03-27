import docker
import mock
import pytest
import uuid

from api_server.addons.providers.exceptions import AddonProviderError

from docker_addons.containers.base import BaseContainer
from docker_addons.models import ContainerInfo
from docker_addons.provider import DockerAddonProvider


@pytest.fixture(scope='function')
def fake_type():
    return mock.MagicMock()


@pytest.fixture(scope='function')
def fake_container(fake_type):
    container = mock.Mock(spec=BaseContainer)
    fake_type.get_container.return_value = container
    return container


@pytest.fixture(scope='function')
def provider(fake_type):
    return DockerAddonProvider(fake_type, 'DATABASE_URL')


@pytest.fixture(scope='function')
def fake_container_info():
    info = mock.Mock(spec=ContainerInfo)
    info.uuid = uuid.uuid4()
    return info


def test_begin_provision_success(provider, fake_container_info, fake_container):
    with mock.patch('docker_addons.provider.ContainerInfo.objects.create') as mocked:
        mocked.return_value = fake_container_info
        result = provider.begin_provision(None)
    assert 'message' in result
    assert result['uuid'] == fake_container_info.uuid
    fake_container.run_container.assert_called_once_with()


def test_begin_provision_errors(provider, fake_container_info, fake_container):
    fake_container.run_container.side_effect = docker.errors.DockerException
    with mock.patch('docker_addons.provider.ContainerInfo.objects.create') as mocked:
        mocked.return_value = fake_container_info
        with pytest.raises(AddonProviderError):
            provider.begin_provision(None)


def test_get_config_success(provider, fake_container_info, fake_container):
    hostname = 'hostname'
    fake_container.get_docker_hostname.return_value = hostname
    with mock.patch('docker_addons.provider.ContainerInfo.objects.get') as mocked:
        mocked.return_value = fake_container_info
        result = provider.get_config(None)
    assert result['config']['DATABASE_URL'] == hostname
    fake_container.get_docker_hostname.assert_called_once_with()


def test_get_config_error(provider, fake_container_info, fake_container):
    with mock.patch('docker_addons.provider.ContainerInfo.objects.get') as mocked:
        mocked.side_effect = ContainerInfo.DoesNotExist
        with pytest.raises(AddonProviderError):
            provider.get_config(None)


def test_deprovision_success(provider, fake_container_info, fake_container):
    with mock.patch('docker_addons.provider.ContainerInfo.objects.get') as mocked:
        mocked.return_value = fake_container_info
        result = provider.deprovision(None)
    assert 'message' in result
    fake_container.stop_container.assert_called_once_with()


def test_deprovision_error(provider, fake_container_info, fake_container):
    with mock.patch('docker_addons.provider.ContainerInfo.objects.get') as mocked:
        mocked.return_value = fake_container_info
        mocked.side_effect = ContainerInfo.DoesNotExist
        with pytest.raises(AddonProviderError):
            provider.deprovision(None)
