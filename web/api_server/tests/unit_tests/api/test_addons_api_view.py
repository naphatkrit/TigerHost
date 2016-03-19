import json
import mock
import pytest
import uuid

from api_server.addons.state import AddonState
from api_server.models import Addon


@pytest.mark.django_db
def test_GET(client, http_headers, app_id, make_app, user):
    """
    @type client: django.test.Client
    @type http_headers: dict
    """
    addons = [Addon.objects.create(provider_name='test_provider', provider_uuid=uuid.uuid4(
    ), app=make_app, state=AddonState.waiting_for_provision, user=user) for _ in range(5)]

    # create some addons that should not be visible
    Addon.objects.create(provider_name='test_provider', provider_uuid=uuid.uuid4(
    ), app=make_app, state=AddonState.deprovisioned, user=user)
    Addon.objects.create(provider_name='test_provider', provider_uuid=uuid.uuid4(
    ), app=make_app, state=AddonState.error, user=user)

    resp = client.get('/api/v1/apps/{}/addons/'.format(app_id), **http_headers)
    assert resp.status_code == 200
    assert resp.json()['results'] == [x.to_dict() for x in addons]


@pytest.mark.django_db
def test_POST(client, http_headers, app_id, make_app, mock_manager, mock_addon_provider):
    """
    @type client: django.test.Client
    @type http_headers: dict
    """
    mock_addon_provider.begin_provision.return_value = {
        'message': 'test message',
        'uuid': uuid.uuid4(),
    }
    with mock.patch('api_server.api.addons_api_view.StateMachineManager') as mocked:
        mocked.return_value = mock_manager
        with mock.patch('api_server.api.addons_api_view.get_provider_from_provider_name') as mock_get_provider:
            mock_get_provider.return_value = mock_addon_provider
            resp = client.post('/api/v1/apps/{}/addons/'.format(app_id), data=json.dumps(
                {'provider_name': 'test_provider'}), content_type='application/json', **http_headers)
    assert resp.status_code == 200
    result = resp.json()
    assert result['message'] == 'test message'
    assert 'addon' in result

    mock_addon_provider.begin_provision.assert_called_once_with(app_id)
    assert mock_manager.start_task.call_count == 1
