import pytest


def pytest_addoption(parser):
    parser.addoption('--api-server-url', action='store', required=True,
                     default=None, help="URL for the local api server instance.")
    parser.addoption('--test-username', action='store', required=True,
                     default=None, help="Username for the test user on the api server.")
    parser.addoption('--test-api-key', action='store', required=True,
                     default=None, help="API key for the test user on the api server.")


@pytest.fixture
def api_server_url(request):
    return request.config.getoption("--api-server-url")


@pytest.fixture
def username(request):
    return request.config.getoption("--test-username")


@pytest.fixture
def api_key(request):
    return request.config.getoption("--test-api-key")
