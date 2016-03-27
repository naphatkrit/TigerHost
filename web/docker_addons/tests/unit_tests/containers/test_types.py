import pytest

from docker_addons.containers.types import AddonTypes


@pytest.mark.django_db
def test_get_container_complete(container_info, fake_docker_client, network_name):
    for x in AddonTypes:
        assert x.get_container(
            container_info=container_info,
            docker_client=fake_docker_client,
            network_name=network_name) is not None
