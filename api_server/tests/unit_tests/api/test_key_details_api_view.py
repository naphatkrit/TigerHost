import mock
import pytest


@pytest.mark.xfail(reason='provider model refactor')
@pytest.mark.django_db
def test_DELETE(client, http_headers, mock_deis_authenticated_client):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_deis_authenticated_client: mock.Mock
    """
    key_name = 'mbp'
    with mock.patch('api_server.api.api_base_view.ApiBaseView.deis_client') as mock_deis_client:
        mock_deis_client.login_or_register.return_value = mock_deis_authenticated_client, False
        resp = client.delete(
            '/api/v1/keys/{}/'.format(key_name), **http_headers)
    assert resp.status_code == 204
    mock_deis_authenticated_client.remove_key.asseassert_called_once_with(
        key_name)
