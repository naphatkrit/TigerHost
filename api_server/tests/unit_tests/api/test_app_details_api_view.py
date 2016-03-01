import json
import mock
import pytest

from api_server.models import App


@pytest.mark.django_db
def test_GET(client, http_headers, mock_provider_authenticated_client, app_id, make_app):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_provider_authenticated_client: mock.Mock
    """
    owner = 'userid'
    mock_provider_authenticated_client.get_application_owner.return_value = owner
    with mock.patch('api_server.api.app_details_api_view.get_provider_authenticated_client') as mocked:
        mocked.return_value = mock_provider_authenticated_client
        resp = client.get('/api/v1/apps/{}/'.format(app_id), **http_headers)
    assert resp.status_code == 200
    assert resp.json() == {
        'owner': owner,
        'remote': 'ssh://git@fake.example.com:2222/{}.git'.format(app_id),
    }
    mock_provider_authenticated_client.get_application_owner.assert_called_once_with(
        app_id)


@pytest.mark.django_db
def test_POST(client, http_headers, mock_provider_authenticated_client, user2, make_app, app_id):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_provider_authenticated_client: mock.Mock
    """
    owner = user2.username
    with mock.patch('api_server.api.app_details_api_view.get_provider_authenticated_client') as mocked:
        mocked.return_value = mock_provider_authenticated_client
        resp = client.post('/api/v1/apps/{}/'.format(app_id),
                           data=json.dumps({'owner': owner}),
                           content_type='application/json',
                           **http_headers)
    assert resp.status_code == 204
    mock_provider_authenticated_client.set_application_owner.assert_called_once_with(
        app_id, owner)


@pytest.mark.django_db
def test_POST_no_user(client, http_headers, mock_provider_authenticated_client, make_app, app_id):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_provider_authenticated_client: mock.Mock
    """
    owner = 'does_not_exist'
    with mock.patch('api_server.api.app_details_api_view.get_provider_authenticated_client') as mocked:
        mocked.return_value = mock_provider_authenticated_client
        resp = client.post('/api/v1/apps/{}/'.format(app_id),
                           data=json.dumps({'owner': owner}),
                           content_type='application/json',
                           **http_headers)
    assert resp.status_code == 400


@pytest.mark.django_db
def test_DELETE(client, http_headers, mock_provider_authenticated_client, make_app, app_id):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_provider_authenticated_client: mock.Mock
    """
    assert App.objects.filter(app_id=app_id).count() == 1
    with mock.patch('api_server.api.app_details_api_view.get_provider_authenticated_client') as mocked:
        mocked.return_value = mock_provider_authenticated_client
        resp = client.delete('/api/v1/apps/{}/'.format(app_id), **http_headers)
    assert resp.status_code == 204
    mock_provider_authenticated_client.delete_application.assert_called_once_with(
        app_id)
    assert App.objects.filter(app_id=app_id).count() == 0
