import pytest

from docker_addons.containers.mongo import MongoContainer


@pytest.fixture(scope='function')
def container(container_info, fake_docker_client, network_name):
    return MongoContainer(container_info, fake_docker_client, network_name)


@pytest.mark.django_db
def test_get_url(container, container_info):
    assert container.get_url() == 'mongodb://{}:default@{}:27017/mongo_db'.format(
        container_info.name,
        container.get_docker_hostname())
