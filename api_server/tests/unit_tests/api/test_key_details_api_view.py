import mock
import pytest


@pytest.mark.django_db
def test_DELETE(client, http_headers, mock_provider_authenticated_client, settings):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_provider_authenticated_client: mock.Mock
    """
    key_name = 'mbp'
    with mock.patch('api_server.api.key_details_api_view.get_provider_authenticated_client') as mocked:
        mocked.return_value = mock_provider_authenticated_client
        resp = client.delete(
            '/api/v1/keys/{}/{}/'.format(settings.DEFAULT_PAAS_PROVIDER, key_name), **http_headers)
    assert resp.status_code == 204
    mock_provider_authenticated_client.remove_key.asseassert_called_once_with(
        key_name)
