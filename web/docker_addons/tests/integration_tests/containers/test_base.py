import docker
import pytest

from docker_addons.containers.base import BaseContainer


@pytest.fixture
def docker_client():
    return docker.from_env(assert_hostname=False)


@pytest.fixture(scope='function')
def network_name():
    return 'default'


@pytest.fixture(scope='function')
def container(container_info, docker_client, network_name):
    class TestingContainer(BaseContainer):

        def get_environment(self):
            return {
                'POSTGRES_USER': self.container_info.name
            }

        def get_image(self):
            """Get the image for this container

            @rtype: str
            """
            return 'postgres:9.5'

        def get_url(self):
            """Return the URL to connect to this container, in the correct protocol

            @rtype: str
            """
            return 'http://fake'
    return TestingContainer(container_info, docker_client, network_name)


@pytest.mark.django_db
def test_run_container(container, container_info):
    container.run_container()
    container_info.refresh_from_db()
    assert container_info.container_id is not None
    container.stop_container()
