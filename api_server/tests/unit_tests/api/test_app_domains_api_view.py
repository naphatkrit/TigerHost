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
    domains = ['example.com', 'example2.com']
    mock_provider_authenticated_client.get_application_domains.return_value = domains
    with mock.patch('api_server.api.app_domains_api_view.get_provider_authenticated_client') as mocked:
        mocked.return_value = mock_provider_authenticated_client
        resp = client.get('/api/v1/apps/{}/domains/'.format(app_id), **http_headers)
    assert resp.status_code == 200
    assert set(resp.json()['results']) == set(domains)
    mock_provider_authenticated_client.get_application_domains.assert_called_once_with(app_id)


@pytest.mark.django_db
def test_POST(client, http_headers, mock_provider_authenticated_client, app_id, make_app):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_provider_authenticated_client: mock.Mock
    """
    domain = 'example.com'
    with mock.patch('api_server.api.app_domains_api_view.get_provider_authenticated_client') as mocked:
        mocked.return_value = mock_provider_authenticated_client
        resp = client.post('/api/v1/apps/{}/domains/'.format(app_id), data=json.dumps({
            'domain': domain
        }), content_type='application/json', **http_headers)
    assert resp.status_code == 204
    mock_provider_authenticated_client.add_application_domain.assert_called_once_with(
        app_id, domain)
