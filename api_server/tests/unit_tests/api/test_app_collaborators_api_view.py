import json
import mock
import pytest


@pytest.mark.django_db
def test_GET(client, http_headers, mock_backend_authenticated_client, app_id, make_app):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_backend_authenticated_client: mock.Mock
    """
    users = ['username1', 'username2']
    mock_backend_authenticated_client.get_application_collaborators.return_value = users
    with mock.patch('api_server.api.app_collaborators_api_view.get_backend_authenticated_client') as mocked:
        mocked.return_value = mock_backend_authenticated_client
        resp = client.get(
            '/api/v1/apps/{}/collaborators/'.format(app_id), **http_headers)
    assert resp.status_code == 200
    assert set(resp.json()['results']) == set(users)
    mock_backend_authenticated_client.get_application_collaborators.assert_called_once_with(
        app_id)


@pytest.mark.django_db
def test_POST(client, http_headers, mock_backend_authenticated_client, user2, app_id, make_app):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_backend_authenticated_client: mock.Mock
    """
    user = user2.username
    with mock.patch('api_server.api.app_collaborators_api_view.get_backend_authenticated_client') as mocked:
        mocked.return_value = mock_backend_authenticated_client
        resp = client.post('/api/v1/apps/{}/collaborators/'.format(app_id), data=json.dumps(
            {'username': user}), content_type='application/json', **http_headers)
    assert resp.status_code == 204
    mock_backend_authenticated_client.add_application_collaborator.assert_called_once_with(
        app_id, user)


@pytest.mark.django_db
def test_POST_no_user(client, http_headers, mock_backend_authenticated_client, app_id, make_app):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_backend_authenticated_client: mock.Mock
    """
    user = 'doesnotexist'
    with mock.patch('api_server.api.app_collaborators_api_view.get_backend_authenticated_client') as mocked:
        mocked.return_value = mock_backend_authenticated_client
        resp = client.post('/api/v1/apps/{}/collaborators/'.format(app_id), data=json.dumps(
            {'username': user}), content_type='application/json', **http_headers)
    assert resp.status_code == 400
    assert user in resp.content
