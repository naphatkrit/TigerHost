import json
import mock
import pytest


@pytest.mark.django_db
def test_GET(client, http_headers, mock_deis_authenticated_client):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_deis_authenticated_client: mock.Mock
    """
    bindings = {
        'VAR1': 'value1',
        'VAR2': 'value2',
    }
    mock_deis_authenticated_client.get_application_env_variables.return_value = bindings
    with mock.patch('api_server.api.api_base_view.ApiBaseView.deis_client') as mock_deis_client:
        mock_deis_client.login_or_register.return_value = mock_deis_authenticated_client, False
        resp = client.get('/api/v1/apps/testid/env/', **http_headers)
    assert resp.status_code == 200
    assert resp.json() == bindings


@pytest.mark.django_db
def test_POST(client, http_headers, mock_deis_authenticated_client):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_deis_authenticated_client: mock.Mock
    """
    bindings = {
        'VAR1': 'value1',
        'VAR2': 'value2',
    }
    with mock.patch('api_server.api.api_base_view.ApiBaseView.deis_client') as mock_deis_client:
        mock_deis_client.login_or_register.return_value = mock_deis_authenticated_client, False
        resp = client.post('/api/v1/apps/testid/env/', data=json.dumps(bindings), content_type='application/json', **http_headers)
    assert resp.status_code == 204
    mock_deis_authenticated_client.set_application_env_variables.assert_called_once_with('testid', bindings)
