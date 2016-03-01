import mock
import pytest
import requests

from api_server.clients.deis_client_errors import DeisClientResponseError


@pytest.fixture
def mock_response():
    mocked = mock.Mock(spec=requests.Response)
    mocked.status_code = 400
    mocked.json.return_value = {
        'error': 'sample error'
    }
    return mocked


@pytest.mark.django_db
def test_deis_client_response_error(client, http_headers, mock_response):
    with mock.patch('api_server.api.apps_api_view.get_provider_authenticated_client') as mocked:
        mocked.side_effect = DeisClientResponseError(
            mock_response)
        resp = client.get('/api/v1/apps/', **http_headers)
    assert resp.status_code == 400
    assert resp.json() == {
        'error': 'sample error'
    }
