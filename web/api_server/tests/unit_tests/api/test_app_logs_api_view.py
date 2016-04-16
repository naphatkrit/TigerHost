import mock
import pytest


@pytest.mark.django_db
def test_GET(client, http_headers, mock_backend_authenticated_client, app_id, make_app):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_backend_authenticated_client: mock.Mock
    """
    logs = ['entry1', 'entry2']
    mock_backend_authenticated_client.get_application_logs.return_value = logs
    with mock.patch('api_server.api.app_logs_api_view.get_backend_authenticated_client') as mocked:
        mocked.return_value = mock_backend_authenticated_client
        resp = client.get(
            '/api/v1/apps/{}/logs/'.format(app_id), **http_headers)
    assert resp.status_code == 200
    assert resp.json()['results'] == logs
    mock_backend_authenticated_client.get_application_logs.assert_called_once_with(
        app_id, None)


@pytest.mark.django_db
def test_GET_with_params(client, http_headers, mock_backend_authenticated_client, app_id, make_app):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_backend_authenticated_client: mock.Mock
    """
    logs = ['entry1', 'entry2']
    mock_backend_authenticated_client.get_application_logs.return_value = logs
    with mock.patch('api_server.api.app_logs_api_view.get_backend_authenticated_client') as mocked:
        mocked.return_value = mock_backend_authenticated_client
        resp = client.get('/api/v1/apps/{}/logs/'.format(app_id),
                          {'lines': 20}, **http_headers)
    assert resp.status_code == 200
    assert resp.json()['results'] == logs
    mock_backend_authenticated_client.get_application_logs.assert_called_once_with(
        app_id, 20)
