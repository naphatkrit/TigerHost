import json
import mock
import pytest

from api_server.models import App


@pytest.mark.django_db
def test_GET(client, http_headers, mock_backend_authenticated_client, settings):
    mock_backend_authenticated_client.get_all_applications.return_value = ['app1', 'app2']
    with mock.patch('api_server.api.apps_api_view.get_backend_authenticated_client') as mocked:
        mocked.return_value = mock_backend_authenticated_client
        resp = client.get('/api/v1/apps/', **http_headers)
    assert resp.status_code == 200
    assert resp.json() == {
        settings.DEFAULT_PAAS_BACKEND: ['app1', 'app2']
    }
    mock_backend_authenticated_client.get_all_applications.asserassert_called_once_with('apps')


@pytest.mark.django_db
def test_POST_success(client, http_headers, mock_backend_authenticated_client, settings):
    with mock.patch('api_server.api.apps_api_view.get_backend_authenticated_client') as mocked:
        mocked.return_value = mock_backend_authenticated_client
        resp = client.post('/api/v1/apps/', data=json.dumps({
            'id': 'sample-id'
        }), content_type='application/json', **http_headers)
    assert resp.status_code == 204
    mock_backend_authenticated_client.create_application.assert_called_once_with('sample-id')
    assert App.get_backend('sample-id') == settings.DEFAULT_PAAS_BACKEND


@pytest.mark.django_db
def test_POST_failure_auth_client(client, http_headers, mock_backend_authenticated_client, settings):
    with mock.patch('api_server.api.apps_api_view.get_backend_authenticated_client') as mocked:
        mocked.return_value = mock_backend_authenticated_client
        mock_backend_authenticated_client.create_application.side_effect = Exception
        resp = client.post('/api/v1/apps/', data=json.dumps({
            'id': 'sample-id'
        }), content_type='application/json', **http_headers)
    assert resp.status_code == 500
    mock_backend_authenticated_client.create_application.assert_called_once_with('sample-id')
    assert App.objects.filter(app_id='sample-id').count() == 0
