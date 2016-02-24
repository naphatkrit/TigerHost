import pytest

from django.utils import crypto


@pytest.fixture
def fake_deis_url():
    return "http://fake"


@pytest.fixture(scope='function')
def token():
    return crypto.get_random_string()
