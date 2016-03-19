import pytest

from aws_db_addons.models import DbInstance


@pytest.fixture(scope='function')
def db_instance():
    return DbInstance.objects.create()
