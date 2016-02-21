import pytest


def pytest_addoption(parser):
    parser.addoption('--deis-url', action='store', required=True,
                     default=None, help="URL for the local deis instance.")


@pytest.fixture
def deis_url(request):
    return request.config.getoption("--deis-url")
