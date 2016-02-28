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
    owner = 'userid'
    mock_deis_authenticated_client.get_application_owner.return_value = owner
    with mock.patch('api_server.api.api_base_view.ApiBaseView.deis_client') as mock_deis_client:
        mock_deis_client.login_or_register.return_value = mock_deis_authenticated_client, False
        mock_deis_client.deis_url = 'http://fake'
        resp = client.get('/api/v1/apps/testid/', **http_headers)
    assert resp.status_code == 200
    assert resp.json() == {
        'owner': owner,
        'remote': 'ssh://git@fake:2222/testid.git',
    }


@pytest.mark.django_db
def test_POST(client, http_headers, mock_deis_authenticated_client, user2):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_deis_authenticated_client: mock.Mock
    """
    owner = user2.username
    with mock.patch('api_server.api.api_base_view.ApiBaseView.deis_client') as mock_deis_client:
        mock_deis_client.login_or_register.return_value = mock_deis_authenticated_client, False
        resp = client.post('/api/v1/apps/testid/',
                           data=json.dumps({'owner': owner}),
                           content_type='application/json',
                           **http_headers)
    assert resp.status_code == 204
    mock_deis_authenticated_client.set_application_owner.assert_called_once_with(
        'testid', owner)


@pytest.mark.django_db
def test_POST_no_user(client, http_headers, mock_deis_authenticated_client):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_deis_authenticated_client: mock.Mock
    """
    owner = 'does_not_exist'
    with mock.patch('api_server.api.api_base_view.ApiBaseView.deis_client') as mock_deis_client:
        mock_deis_client.login_or_register.return_value = mock_deis_authenticated_client, False
        resp = client.post('/api/v1/apps/testid/',
                           data=json.dumps({'owner': owner}),
                           content_type='application/json',
                           **http_headers)
    assert resp.status_code == 404


@pytest.mark.django_db
def test_DELETE(client, http_headers, mock_deis_authenticated_client):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_deis_authenticated_client: mock.Mock
    """
    with mock.patch('api_server.api.api_base_view.ApiBaseView.deis_client') as mock_deis_client:
        mock_deis_client.login_or_register.return_value = mock_deis_authenticated_client, False
        resp = client.delete('/api/v1/apps/testid/', **http_headers)
    assert resp.status_code == 204
    mock_deis_authenticated_client.delete_application.assert_called_once_with(
        'testid')
