import mock
import pytest

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


@pytest.fixture(scope='function')
def public_key(username):
    # taken randomly from the internet
    return """ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAyyA8wePstPC69PeuHFtOwyTecByonsHFAjHbVnZ+h0dpomvLZxUtbknNj3+c7MPYKqKBOx9gUKV/diR/mIDqsb405MlrI1kmNR9zbFGYAAwIH/Gxt0Lv5ffwaqsz7cECHBbMojQGEz3IH3twEvDfF6cu5p00QfP0MSmEi/eB+W+h30NGdqLJCziLDlp409jAfXbQm/4Yx7apLvEmkaYSrb5f/pfvYv1FEV1tS8/J7DgdHUAWo6gyGUUSZJgsyHcuJT7v9Tf0xwiFWOWL9WsWXa9fCKqTeYnYJhHlqfinZRnT/+jkz0OZ7YmXo6j4Hyms3RCOqenIX1W6gnIn+eQIkw== This is the key's comment{}
""".format(username)


@pytest.yield_fixture(autouse=True)
def settings(api_server_url):
    with mock.patch('tigerhost.settings.API_SERVER_URL', new=api_server_url):
        yield
