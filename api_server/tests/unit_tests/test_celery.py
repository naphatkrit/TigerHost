import pytest

from api_server.celery import debug_task


@pytest.mark.django_db
def test_debug_task():
    debug_task.delay()
