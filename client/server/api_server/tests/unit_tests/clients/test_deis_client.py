import json
import mock
import requests
import responses
import pytest
import urlparse

from api_server.clients.deis_client import DeisClient
from api_server.clients.deis_client_errors import DeisClientError, DeisClientTimeoutError, DeisClientResponseError


@pytest.fixture
def deis_client(fake_deis_url):
    return DeisClient(fake_deis_url)


@responses.activate
def test_request_and_raise_failure_response(deis_client, fake_deis_url):
    path = 'v1/auth/register/'
    responses.add(responses.POST, urlparse.urljoin(
        fake_deis_url, path), status=400)
    with pytest.raises(DeisClientResponseError):
        deis_client._request_and_raise('POST', path)


def test_request_and_raise_failure_generic(deis_client, fake_deis_url):
    with mock.patch('requests.request') as mock_request:
        mock_request.side_effect = requests.exceptions.RequestException
        path = 'v1/auth/register/'
        with pytest.raises(DeisClientError):
            deis_client._request_and_raise('POST', path)


def test_request_and_raise_failure_timeout(deis_client, fake_deis_url):
    with mock.patch('requests.request') as mock_request:
        mock_request.side_effect = requests.exceptions.Timeout
        path = 'v1/auth/register/'
        with pytest.raises(DeisClientTimeoutError):
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


@responses.activate
def test_login_or_register_not_created(deis_client, fake_deis_url, username, password, email):
    """
    @type deis_client: DeisClient
    @type fake_deis_url: str
    @type username: str
    @type password: str
    @type email: str
    """
    responses.add(responses.POST, urlparse.urljoin(
        fake_deis_url, 'v1/auth/login/'), status=201, json={"token": "sometoken"})
    auth_client, created = deis_client.login_or_register(
        username, password, email)
    assert not created
    assert auth_client.token == 'sometoken'


@responses.activate
def test_login_or_register_created(deis_client, fake_deis_url, username, password, email):
    """
    @type deis_client: DeisClient
    @type fake_deis_url: str
    @type username: str
    @type password: str
    @type email: str
    """
    count = [0]

    def request_callback(request):
        if count[0] == 0:
            count[0] += 1
            return (400, {}, '')
        return (201, {}, json.dumps({'token': 'sometoken'}))

    responses.add_callback(responses.POST, urlparse.urljoin(fake_deis_url, 'v1/auth/login/'),
                           content_type='application/json', callback=request_callback)
    responses.add(responses.POST, urlparse.urljoin(
        fake_deis_url, 'v1/auth/register/'), status=201)
    auth_client, created = deis_client.login_or_register(
        username, password, email)
    assert created
    assert auth_client.token == 'sometoken'
