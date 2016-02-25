import pytest
import responses
import urlparse

from tigerhost.api_client import ApiClient, ApiClientResponseError, ApiClientAuthenticationError


@pytest.fixture()
def fake_api_server_url():
    return 'http://fake'


@pytest.fixture()
def api_client(fake_api_server_url):
    return ApiClient(username='', api_key='', api_server_url=fake_api_server_url)


@responses.activate
def test_request_and_raise_failure(api_client, fake_api_server_url):
    path = 'v1/auth/register/'
    responses.add(responses.POST, urlparse.urljoin(
        fake_api_server_url, path), status=400)
    with pytest.raises(ApiClientResponseError):
        api_client._request_and_raise('POST', path)


@responses.activate
def test_request_and_raise_failure_authentication(api_client, fake_api_server_url):
    path = 'v1/auth/register/'
    responses.add(responses.POST, urlparse.urljoin(
        fake_api_server_url, path), status=401)
    with pytest.raises(ApiClientAuthenticationError):
        api_client._request_and_raise('POST', path)


@responses.activate
def test_test_api_key_success(api_client, fake_api_server_url):
    """
    @type api_client: ApiClient
    @type fake_api_server_url: str
    """
    responses.add(responses.GET, urlparse.urljoin(
        fake_api_server_url, 'api/test_api_key/'), status=200)
    api_client.test_api_key()


@responses.activate
def test_get_all_applications_success(api_client, fake_api_server_url):
    """
    @type api_client: ApiClient
    @type fake_api_server_url: str
    """
    test_ids = ['testid1', 'testid2']
    responses.add(responses.GET, urlparse.urljoin(
        fake_api_server_url, 'api/v1/apps'), status=200, json={
        "results": test_ids
    })
    ids = api_client.get_all_applications()
    assert set(ids) == set(test_ids)
