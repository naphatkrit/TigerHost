import pytest


@pytest.fixture
def deis_mocked_url():
    # TODO should be random
    return "http://deis.mocked.deisapp.com"


@pytest.fixture
def deis_url(request, deis_mocked_url):
    url = request.config.getoption("--deis-url")
    return url if url is not None else deis_mocked_url
