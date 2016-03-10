import pytest

from aws_db_addons.models import DbInstance


@pytest.mark.django_db
def test_db_instance():
    for _ in range(10):
        instance = DbInstance.objects.create()
        assert len(instance.master_username) == 16
        assert len(instance.master_password) == 30
        assert len(instance.aws_instance_identifier) == 63
        assert len(instance.db_name) == 64
