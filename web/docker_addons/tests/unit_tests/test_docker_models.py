import pytest

from docker_addons.models import ContainerInfo


@pytest.mark.django_db
def test_container_info():
    seen = set()
    for _ in range(30):
        instance = ContainerInfo.objects.create()
        assert len(instance.name) == 50
        assert instance.name not in seen
        seen.add(instance.name)
