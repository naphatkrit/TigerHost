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
    domains = ['example.com', 'example2.com']
    mock_deis_authenticated_client.get_application_domains.return_value = domains
    with mock.patch('api_server.api.api_base_view.ApiBaseView.deis_client') as mock_deis_client:
        mock_deis_client.login_or_register.return_value = mock_deis_authenticated_client, False
        resp = client.get('/api/v1/apps/testid/domains/', **http_headers)
    assert resp.status_code == 200
    assert set(resp.json()['results']) == set(domains)


@pytest.mark.django_db
def test_POST(client, http_headers, mock_deis_authenticated_client):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_deis_authenticated_client: mock.Mock
    """
    domain = 'example.com'
    with mock.patch('api_server.api.api_base_view.ApiBaseView.deis_client') as mock_deis_client:
        mock_deis_client.login_or_register.return_value = mock_deis_authenticated_client, False
        resp = client.post('/api/v1/apps/testid/domains/', data=json.dumps({
            'domain': domain
        }), content_type='application/json', **http_headers)
    assert resp.status_code == 204
    mock_deis_authenticated_client.add_application_domain.assert_called_once_with(
        'testid', domain)
