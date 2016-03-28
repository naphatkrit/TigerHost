import pytest

from docker_addons.containers.postgres import PostgresContainer


@pytest.fixture(scope='function')
def container(container_info, fake_docker_client, network_name):
    return PostgresContainer(container_info, fake_docker_client, network_name)


@pytest.mark.django_db
def test_get_url(container, container_info):
    assert container.get_url() == 'postgres://{}@{}:5432/postgresdb'.format(
        container_info.name,
        container.get_docker_hostname())
