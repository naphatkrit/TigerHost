import json
import mock
import pytest


@pytest.mark.django_db
def test_GET(client, http_headers, mock_provider_authenticated_client):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_provider_authenticated_client: mock.Mock
    """
    keys = [
        {'key_name': 'mbp1', 'key': 'ssh-rsa1'},
        {'key_name': 'mbp2', 'key': 'ssh-rsa2'},
    ]
    mock_provider_authenticated_client.get_keys.return_value = keys
    with mock.patch('api_server.api.keys_api_view.get_provider_authenticated_client') as mocked:
        mocked.return_value = mock_provider_authenticated_client
        resp = client.get('/api/v1/keys/', **http_headers)
    assert resp.status_code == 200
    assert resp.json()['results'] == keys
    mock_provider_authenticated_client.get_keys.assert_called_once_with()


@pytest.mark.django_db
def test_POST(client, http_headers, mock_provider_authenticated_client):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_provider_authenticated_client: mock.Mock
    """
    key = {'key_name': 'mbp', 'key': 'ssh-rsa1'}
    with mock.patch('api_server.api.keys_api_view.get_provider_authenticated_client') as mocked:
        mocked.return_value = mock_provider_authenticated_client
        resp = client.post('/api/v1/keys/',
                           data=json.dumps(key),
                           content_type='application/json',
                           **http_headers)
    assert resp.status_code == 204
    mock_provider_authenticated_client.add_key.assert_called_once_with(
        'mbp', 'ssh-rsa1')
