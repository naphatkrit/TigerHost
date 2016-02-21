import pytest

from django.utils import crypto

from api_server.clients.deis_client import DeisClient
from api_server.clients.deis_client_errors import DeisClientResponseError


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


def test_register(deis_client, username, password, email):
    """@type deis_client: DeisClient
    """
    # register one user
    deis_client.register(username, password, email)

    # test the failure case when we register a user twice
    with pytest.raises(DeisClientResponseError):
        deis_client.register(username, "any", "any")
