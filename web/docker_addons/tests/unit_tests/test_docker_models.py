import pytest

from docker_addons.models import Container


@pytest.mark.django_db
def test_db_instance():
    seen = set()
    for _ in range(30):
        instance = Container.objects.create()
        assert len(instance.name) == 50
        assert instance.name not in seen
        seen.add(instance.name)
