import pytest

from django.utils import crypto

@pytest.fixture
def fake_deis_url():
    return "http://fake"


@pytest.fixture(scope='function')
def username():
    return crypto.get_random_string()


@pytest.fixture(scope='function')
def email(username):
    return '{}@princeton.edu'.format(username)


@pytest.fixture(scope='function')
def password():
    return crypto.get_random_string()


@pytest.fixture(scope='function')
def token():
    return crypto.get_random_string()
