import mock
import pytest
import random
import string

from tigerhost.api_client import ApiClient


def pytest_addoption(parser):
    parser.addoption('--api-server-url', action='store', required=True,
                     default=None, help="URL for the local api server instance.")
    parser.addoption('--test-username', action='store', required=True,
                     default=None, help="Username for the test user on the api server.")
    parser.addoption('--test-api-key', action='store', required=True,
                     default=None, help="API key for the test user on the api server.")
    parser.addoption('--test-username2', action='store', required=True,
                     default=None, help="Username for the second test user on the api server.")
    parser.addoption('--test-api-key2', action='store', required=True,
                     default=None, help="API key for the second test user on the api server.")


@pytest.fixture
def api_server_url(request):
    return request.config.getoption("--api-server-url")


@pytest.fixture
def username(request):
    return request.config.getoption("--test-username")


@pytest.fixture
def api_key(request):
    return request.config.getoption("--test-api-key")


@pytest.fixture
def username2(request):
    return request.config.getoption("--test-username2")


@pytest.fixture
def api_key2(request):
    return request.config.getoption("--test-api-key2")


@pytest.fixture(autouse=True)
def api_client(api_server_url, username, api_key):
    client = ApiClient(api_server_url, username, api_key)
    client.test_api_key()
    return client


@pytest.fixture()
def api_client2(api_server_url, username2, api_key2):
    client = ApiClient(api_server_url, username2, api_key2)
    client.test_api_key()
    return client


@pytest.yield_fixture(autouse=True)
def settings(api_server_url):
    with mock.patch('tigerhost.settings.API_SERVER_URL', new=api_server_url):
        yield


@pytest.fixture(scope='function')
def app_id():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12))


@pytest.fixture(autouse=True)
def delete_all_applications(api_client):
    for _, apps in api_client.get_all_applications().iteritems():
        for a in apps:
            api_client.delete_application(a)
