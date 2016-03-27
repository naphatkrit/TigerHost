import docker
import mock
import pytest

from docker_addons.containers.base import BaseContainer


@pytest.fixture
def fake_docker_url():
    return 'tcp://192.168.99.100:2376'


@pytest.fixture(scope='function')
def fake_docker_client(fake_docker_url):
    fake = mock.Mock(spec=docker.Client)
    fake.base_url = fake_docker_url
    return fake


@pytest.fixture
def network_name():
    return 'default'


@pytest.fixture(scope='function')
def container(container_info, fake_docker_client, network_name):
    class TestingContainer(BaseContainer):

        def get_environment(self):
            return {
                'POSTGRES_USER': self.container_info.name
            }

        def get_image(self):
            return 'postgres:9.5'

        def get_url(self):
            return 'http://fake'
    return TestingContainer(container_info, fake_docker_client, network_name)
