import mock
import pytest


from api_server import providers
from api_server.clients.deis_client_errors import DeisClientError


def test_get_provider_client_simple(settings):
    client = providers.get_provider_client(settings.DEFAULT_PAAS_PROVIDER)
    assert client.provider_url == settings.PAAS_PROVIDERS[
        settings.DEFAULT_PAAS_PROVIDER]['API_URL']


def test_get_provider_client_error_missing():
    with pytest.raises(providers.ProvidersMissingError):
        providers.get_provider_client('doesnotexit')


def test_get_provider_client_error_config(settings):
    settings.PAAS_PROVIDERS['new'] = {
        'API_URL': 'http://example.com',
    }
    with pytest.raises(providers.ProvidersConfigError):
        providers.get_provider_client('new')

    settings.PAAS_PROVIDERS['new'] = {
        'CLIENT': 'api_server.clients.base_client.BaseClient',
    }
    with pytest.raises(providers.ProvidersConfigError):
        providers.get_provider_client('new')

    class DummyObject(object):

        def __init__(self, url):
            pass

    with mock.patch('api_server.providers.import_string') as mocked:
        mocked.return_value = DummyObject
        with pytest.raises(providers.ProvidersConfigError):
            providers.get_provider_client(settings.DEFAULT_PAAS_PROVIDER)


def test_get_provider_client_error_import(settings):
    settings.PAAS_PROVIDERS[settings.DEFAULT_PAAS_PROVIDER][
        'CLIENT'] = 'not.real.class'
    with pytest.raises(providers.ProvidersImportError):
        providers.get_provider_client(settings.DEFAULT_PAAS_PROVIDER)


@pytest.mark.django_db
def test_ensure_user_exists_success(mock_provider_client, mock_provider_authenticated_client, settings, user):
    with mock.patch('api_server.providers.get_provider_client') as mocked:
        mocked.return_value = mock_provider_client
        mock_provider_client.login_or_register.return_value = (
            mock_provider_authenticated_client, True)
        result = providers.get_provider_authenticated_client(
            user.username, settings.DEFAULT_PAAS_PROVIDER)
    assert result == mock_provider_authenticated_client


@pytest.mark.django_db
def test_ensure_user_exists_failure_does_not_exist(settings):
    with pytest.raises(providers.ProvidersUserError):
        providers.get_provider_authenticated_client(
            'doesnotexist', settings.DEFAULT_PAAS_PROVIDER)


@pytest.mark.django_db
def test_ensure_user_exists_failure_no_provider(user):
    with pytest.raises(providers.ProvidersMissingError):
        providers.get_provider_authenticated_client(
            user.username, 'doesnotexist')


@pytest.mark.django_db
def test_ensure_user_exists_failure_no_credentials(client, user, mock_provider_client, settings):
    with mock.patch('api_server.providers.get_provider_client') as mocked:
        mocked.return_value = mock_provider_client
        with pytest.raises(providers.ProvidersUserError):
            providers.get_provider_authenticated_client(
                user.username, 'doesnotexist')


@pytest.mark.django_db
def test_ensure_user_exists_failure_client_error(client, user, mock_provider_client, mock_provider_authenticated_client, settings):
    with mock.patch('api_server.providers.get_provider_client') as mocked:
        mocked.return_value = mock_provider_client
        mock_provider_client.login_or_register.return_value = (
            mock_provider_authenticated_client, True)
        mock_provider_authenticated_client.login_or_register.side_effect = DeisClientError
        providers.get_provider_authenticated_client(
            user.username, settings.DEFAULT_PAAS_PROVIDER)
