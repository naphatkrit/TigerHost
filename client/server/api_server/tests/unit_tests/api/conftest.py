import mock
import pytest

from api_server.clients.deis_authenticated_client import DeisAuthenticatedClient


@pytest.fixture
def mock_deis_authenticated_client():
    mocked = mock.Mock(spec=DeisAuthenticatedClient)
    mocked.get_all_applications.return_value = ['app1', 'app2']
    return mocked
