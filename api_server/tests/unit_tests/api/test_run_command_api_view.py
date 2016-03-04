import json
import mock
import pytest


@pytest.mark.django_db
def test_POST(client, http_headers, mock_provider_authenticated_client, make_app, app_id):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_provider_authenticated_client: mock.Mock
    """
    result = {
        'exit_code': 0,
        'output': '1 2 3\n',
    }
    mock_provider_authenticated_client.run_command.return_value = result
    with mock.patch('api_server.api.run_command_api_view.get_provider_authenticated_client') as mocked:
        mocked.return_value = mock_provider_authenticated_client
        resp = client.post('/api/v1/apps/{}/run/'.format(app_id),
                           data=json.dumps({'command': 'echo 1 2 3'}),
                           content_type='application/json',
                           **http_headers)
    assert resp.status_code == 200
    mock_provider_authenticated_client.run_command.assert_called_once_with(
        app_id, 'echo 1 2 3')
    assert resp.json() == result
