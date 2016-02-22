import responses
import pytest
import urlparse

from api_server.clients.deis_client import DeisClient
from api_server.clients.deis_client_errors import DeisClientResponseError


@pytest.fixture
def deis_client(fake_deis_url):
    return DeisClient(fake_deis_url)


@responses.activate
def test_request_and_raise_failure(deis_client, fake_deis_url):
    path = 'v1/auth/register/'
    responses.add(responses.POST, urlparse.urljoin(
        fake_deis_url, path), status=400)
    with pytest.raises(DeisClientResponseError):
        deis_client._request_and_raise('POST', path)


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
