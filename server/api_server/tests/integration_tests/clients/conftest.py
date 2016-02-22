import pytest

from django.utils import crypto

from api_server.clients.deis_client import DeisClient


@pytest.fixture
def deis_client(deis_url):
    return DeisClient(deis_url)


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
def app_id():
    return crypto.get_random_string(allowed_chars='abcdefghijklmnopqrstuvwxyz1234567890')
