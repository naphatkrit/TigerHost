import responses
import pytest
import urlparse

from django.utils import crypto

from api_server.clients.deis_client import DeisClient
from api_server.clients.deis_client_errors import DeisClientResponseError


@pytest.fixture
def fake_deis_url():
    return "http://fake"


@pytest.fixture
def deis_client(fake_deis_url):
    return DeisClient(fake_deis_url)


@pytest.fixture(scope='function')
def username():
    return crypto.get_random_string()


@pytest.fixture(scope='function')
def email(username):
    return '{}@princeton.edu'.format(username)


@pytest.fixture(scope='function')
def password():
    return crypto.get_random_string()


@responses.activate
def test_register_success(deis_client, fake_deis_url, username, password, email):
    """
    @type deis_client: DeisClient
    @type fake_deis_url: str
    @type username: str
    @type password: str
    @type email: str
    """
    responses.add(responses.POST, urlparse.urljoin(
        fake_deis_url, 'v1/auth/register/'), status=201)
    deis_client.register(username, password, email)


@responses.activate
def test_register_failure(deis_client, fake_deis_url, username, password, email):
    """
    @type deis_client: DeisClient
    @type fake_deis_url: str
    @type username: str
    @type password: str
    @type email: str
    """
    responses.add(responses.POST, urlparse.urljoin(
        fake_deis_url, 'v1/auth/register/'), status=400)
    with pytest.raises(DeisClientResponseError):
        deis_client.register(username, password, email)


@responses.activate
def test_login_success(deis_client, fake_deis_url, username, password):
    """
    @type deis_client: DeisClient
    @type fake_deis_url: str
    @type username: str
    @type password: str
    """
    responses.add(responses.POST, urlparse.urljoin(
        fake_deis_url, 'v1/auth/login/'), status=201, json={"token": "sometoken"})
    auth_client = deis_client.login(username, password)
    assert auth_client.token == 'sometoken'


@responses.activate
def test_login_failure(deis_client, fake_deis_url, username, password):
    """
    @type deis_client: DeisClient
    @type fake_deis_url: str
    @type username: str
    @type password: str
    """
    responses.add(responses.POST, urlparse.urljoin(
        fake_deis_url, 'v1/auth/login/'), status=400)
    with pytest.raises(DeisClientResponseError):
        deis_client.login(username, password)
