import pytest

from docker_addons.models import ContainerInfo


@pytest.fixture(scope='function')
def container_info():
    return ContainerInfo.objects.create()
