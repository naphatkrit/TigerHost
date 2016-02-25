import mock
import pytest


@pytest.mark.django_db
def test_DELETE(client, http_headers, mock_deis_authenticated_client):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_deis_authenticated_client: mock.Mock
    """
    with mock.patch('api_server.api.api_base_view.ApiBaseView.deis_client') as mock_deis_client:
        mock_deis_client.login_or_register.return_value = mock_deis_authenticated_client, False
        resp = client.delete('/api/v1/apps/testid/', **http_headers)
    assert resp.status_code == 204
    mock_deis_authenticated_client.delete_application.assert_called_once_with(
        'testid')
