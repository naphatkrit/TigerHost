import mock
import pytest


@pytest.mark.django_db
def test_GET(client, http_headers, mock_deis_authenticated_client):
    with mock.patch('api_server.api.api_base_view.ApiBaseView.deis_client') as mock_deis_client:
        mock_deis_client.login_or_register.return_value = mock_deis_authenticated_client, False
        resp = client.get('/api/v1/apps/', **http_headers)
    assert resp.status_code == 200
    assert set(resp.json()['results']) == set(mock_deis_authenticated_client.get_all_applications.return_value)
