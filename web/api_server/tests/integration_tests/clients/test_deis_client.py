import pytest

from django.utils import crypto

from api_server.clients.deis_client import DeisClient
from api_server.clients.exceptions import ClientResponseError


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
    """
    @type deis_client: DeisClient
    @type username: str
    @type password: str
    @type email: str
    """
    # register one user
    deis_client.register(username, password, email)

    # test the failure case when we register a user twice
    with pytest.raises(ClientResponseError):
        deis_client.register(username, "any", "any")

    # try logging in
    deis_client.login(username, password)


def test_login_failure(deis_client, username, password):
    """
    @type deis_client: DeisClient
    @type username: str
    @type password: str
    """
    with pytest.raises(ClientResponseError):
        deis_client.login(username, password)


def test_login_or_register(deis_client, username, password, email):
    """
    @type deis_client: DeisClient
    @type username: str
    @type password: str
    @type email: str
    """
    auth, created = deis_client.login_or_register(username, password, email)
    assert created

    auth2, created = deis_client.login_or_register(username, password, email)
    assert not created
    assert auth.token == auth2.token
