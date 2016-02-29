import mock
import pytest
import requests

from django.contrib.auth.models import User

from api_server.api.api_base_view import ApiBaseView
from api_server.clients.deis_client_errors import DeisClientResponseError
from api_server.models import Profile
from api_server.providers import ProvidersError


@pytest.fixture
def mock_response():
    mocked = mock.Mock(spec=requests.Response)
    mocked.status_code = 400
    mocked.json.return_value = {
        'error': 'sample error'
    }
    return mocked


@pytest.mark.xfail(reason='provider model refactor')
@pytest.mark.django_db
def test_deis_client_response_error(client, http_headers, mock_response):
    with mock.patch('api_server.api.api_base_view.ApiBaseView.deis_client') as mock_deis_client:
        mock_deis_client.login_or_register.side_effect = DeisClientResponseError(
            mock_response)
        resp = client.get('/api/v1/apps/', **http_headers)
    assert resp.status_code == 400
    assert resp.json() == {
        'error': 'sample error'
    }


@pytest.mark.django_db
def test_ensure_user_exists_success(client, mock_provider_client, mock_provider_authenticated_client, settings, user):
    api = ApiBaseView()
    with mock.patch('api_server.api.api_base_view.get_provider_client') as mocked:
        mocked.return_value = mock_provider_client
        mock_provider_client.login_or_register.return_value = (
            mock_provider_authenticated_client, True)
        api.ensure_user_exists(user.username, settings.DEFAULT_PAAS_PROVIDER)


@pytest.mark.django_db
def test_ensure_user_exists_failure_does_not_exist(client, settings):
    api = ApiBaseView()
    with pytest.raises(User.DoesNotExist):
        api.ensure_user_exists('doesnotexist', settings.DEFAULT_PAAS_PROVIDER)


@pytest.mark.django_db
def test_ensure_user_exists_failure_no_provider(client, user):
    api = ApiBaseView()
    with pytest.raises(ProvidersError):
        api.ensure_user_exists(user.username, 'doesnotexist')


@pytest.mark.django_db
def test_ensure_user_exists_failure_no_credentials(client, user, mock_provider_client, settings):
    api = ApiBaseView()
    with mock.patch('api_server.api.api_base_view.get_provider_client') as mocked:
        mocked.return_value = mock_provider_client
        with pytest.raises(Profile.NoCredentials):
            api.ensure_user_exists(user.username, 'doesnotexist')


@pytest.mark.django_db
def test_ensure_user_exists_failure_client_error(client, user, mock_provider_client, mock_provider_authenticated_client, settings, mock_response):
    api = ApiBaseView()
    with mock.patch('api_server.api.api_base_view.get_provider_client') as mocked:
        mocked.return_value = mock_provider_client
        mock_provider_client.login_or_register.return_value = (
            mock_provider_authenticated_client, True)
        mock_provider_authenticated_client.login_or_register.side_effect = DeisClientResponseError(
            mock_response)
        api.ensure_user_exists(user.username, settings.DEFAULT_PAAS_PROVIDER)
