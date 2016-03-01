import json
import mock
import pytest


@pytest.mark.django_db
def test_GET(client, http_headers, mock_provider_authenticated_client, app_id, make_app):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_provider_authenticated_client: mock.Mock
    """
    bindings = {
        'VAR1': 'value1',
        'VAR2': 'value2',
    }
    mock_provider_authenticated_client.get_application_env_variables.return_value = bindings
    with mock.patch('api_server.api.app_env_variables_api_view.get_provider_authenticated_client') as mocked:
        mocked.return_value = mock_provider_authenticated_client
        resp = client.get('/api/v1/apps/{}/env/'.format(app_id), **http_headers)
    assert resp.status_code == 200
    assert resp.json() == bindings
    mock_provider_authenticated_client.get_application_env_variables.assert_called_once_with(app_id)


@pytest.mark.django_db
def test_POST(client, http_headers, mock_provider_authenticated_client, app_id, make_app):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_provider_authenticated_client: mock.Mock
    """
    bindings = {
        'VAR1': 'value1',
        'VAR2': 'value2',
    }
    with mock.patch('api_server.api.app_env_variables_api_view.get_provider_authenticated_client') as mocked:
        mocked.return_value = mock_provider_authenticated_client
        resp = client.post('/api/v1/apps/{}/env/'.format(app_id), data=json.dumps(bindings), content_type='application/json', **http_headers)
    assert resp.status_code == 204
    mock_provider_authenticated_client.set_application_env_variables.assert_called_once_with(app_id, bindings)
