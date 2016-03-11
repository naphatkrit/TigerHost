import mock
import pytest

from contextlib import contextmanager


@contextmanager
def mock_context_manager(*args, **kwargs):
    yield


@pytest.mark.django_db
def test_GET(client, http_headers, app_id, make_app, addon):
    """
    @type client: django.test.Client
    @type http_headers: dict
    """
    resp = client.get('/api/v1/apps/{}/addons/{}/'.format(
        app_id,
        addon.display_name
    ), **http_headers)
    assert resp.status_code == 200
    result = resp.json()
    assert result == addon.to_dict()


@pytest.mark.django_db
def test_DELETE(client, http_headers, app_id, make_app, mock_manager, mock_addon_provider, addon):
    """
    @type client: django.test.Client
    @type http_headers: dict
    """
    mock_manager.transition = mock_context_manager
    mock_addon_provider.deprovision.return_value = {
        'message': 'test message',
    }
    with mock.patch('api_server.api.addon_details_api_view.StateMachineManager') as mocked:
        mocked.return_value = mock_manager
        with mock.patch('api_server.api.addon_details_api_view.get_provider_from_provider_name') as mock_get_provider:
            mock_get_provider.return_value = mock_addon_provider
            resp = client.delete(
                '/api/v1/apps/{}/addons/{}/'.format(app_id, addon.display_name), **http_headers)
    assert resp.status_code == 200
    result = resp.json()
    assert result['message'] == 'test message'

    mock_addon_provider.deprovision.assert_called_once_with(
        addon.provider_uuid)
    assert mock_manager.start_task.call_count == 1
