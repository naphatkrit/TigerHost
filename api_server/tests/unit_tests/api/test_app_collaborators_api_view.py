import json
import mock
import pytest


@pytest.mark.xfail(reason='provider model refactor')
@pytest.mark.django_db
def test_GET(client, http_headers, mock_deis_authenticated_client):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_deis_authenticated_client: mock.Mock
    """
    users = ['username1', 'username2']
    mock_deis_authenticated_client.get_application_collaborators.return_value = users
    with mock.patch('api_server.api.api_base_view.ApiBaseView.deis_client') as mock_deis_client:
        mock_deis_client.login_or_register.return_value = mock_deis_authenticated_client, False
        resp = client.get('/api/v1/apps/testid/collaborators/', **http_headers)
    assert resp.status_code == 200
    assert set(resp.json()['results']) == set(users)


@pytest.mark.xfail(reason='provider model refactor')
@pytest.mark.django_db
def test_POST(client, http_headers, mock_deis_authenticated_client, user2):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_deis_authenticated_client: mock.Mock
    """
    user = user2.username
    with mock.patch('api_server.api.api_base_view.ApiBaseView.deis_client') as mock_deis_client:
        mock_deis_client.login_or_register.return_value = mock_deis_authenticated_client, False
        resp = client.post('/api/v1/apps/testid/collaborators/', data=json.dumps(
            {'username': user}), content_type='application/json', **http_headers)
    assert resp.status_code == 204
    mock_deis_authenticated_client.add_application_collaborator.assert_called_once_with(
        'testid', user)


@pytest.mark.xfail(reason='provider model refactor')
@pytest.mark.django_db
def test_POST_no_user(client, http_headers, mock_deis_authenticated_client):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_deis_authenticated_client: mock.Mock
    """
    user = 'usernam1'
    with mock.patch('api_server.api.api_base_view.ApiBaseView.deis_client') as mock_deis_client:
        mock_deis_client.login_or_register.return_value = mock_deis_authenticated_client, False
        resp = client.post('/api/v1/apps/testid/collaborators/', data=json.dumps(
            {'username': user}), content_type='application/json', **http_headers)
    assert resp.status_code == 404
