import json
import mock
import pytest


@pytest.mark.django_db
def test_GET(client, http_headers, mock_backend_authenticated_client, settings):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_backend_authenticated_client: mock.Mock
    """
    keys = [
        {'key_name': 'mbp1', 'key': 'ssh-rsa1'},
        {'key_name': 'mbp2', 'key': 'ssh-rsa2'},
    ]
    mock_backend_authenticated_client.get_keys.return_value = keys
    with mock.patch('api_server.api.keys_api_view.get_backend_authenticated_client') as mocked:
        mocked.return_value = mock_backend_authenticated_client
        resp = client.get('/api/v1/keys/', **http_headers)
    assert resp.status_code == 200
    assert resp.json() == {
        settings.DEFAULT_PAAS_BACKEND: keys
    }
    mock_backend_authenticated_client.get_keys.assert_called_once_with()


@pytest.mark.django_db
def test_POST(username, client, http_headers, mock_backend_authenticated_client, settings):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_backend_authenticated_client: mock.Mock
    """
    key = {'key_name': 'mbp', 'key': 'ssh-rsa1', 'backend': settings.DEFAULT_PAAS_BACKEND}
    with mock.patch('api_server.api.keys_api_view.get_backend_authenticated_client') as mocked:
        mocked.return_value = mock_backend_authenticated_client
        resp = client.post('/api/v1/keys/',
                           data=json.dumps(key),
                           content_type='application/json',
                           **http_headers)
    mocked.assert_called_once_with(username, settings.DEFAULT_PAAS_BACKEND)
    assert resp.status_code == 204
    mock_backend_authenticated_client.add_key.assert_called_once_with(
        'mbp', 'ssh-rsa1')


@pytest.mark.django_db
def test_POST_default_backend(username, client, http_headers, mock_backend_authenticated_client, settings):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_backend_authenticated_client: mock.Mock
    """
    key = {'key_name': 'mbp', 'key': 'ssh-rsa1', 'backend': settings.DEFAULT_PAAS_BACKEND}
    with mock.patch('api_server.api.keys_api_view.get_backend_authenticated_client') as mocked:
        mocked.return_value = mock_backend_authenticated_client
        resp = client.post('/api/v1/keys/',
                           data=json.dumps(key),
                           content_type='application/json',
                           **http_headers)
    mocked.assert_called_once_with(username, settings.DEFAULT_PAAS_BACKEND)
    assert resp.status_code == 204
    mock_backend_authenticated_client.add_key.assert_called_once_with(
        'mbp', 'ssh-rsa1')
