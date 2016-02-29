import mock
import pytest

from api_server.clients.base_client import BaseClient
from api_server.clients.base_authenticated_client import BaseAuthenticatedClient


@pytest.fixture
def mock_provider_authenticated_client():
    mocked = mock.Mock(spec=BaseAuthenticatedClient)
    mocked.get_all_applications.return_value = ['app1', 'app2']
    return mocked


@pytest.fixture
def mock_provider_client():
    return mock.Mock(spec=BaseClient)
