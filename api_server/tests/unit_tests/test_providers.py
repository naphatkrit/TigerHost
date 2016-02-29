import mock
import pytest


from api_server import providers


def test_get_provider_client_simple(settings):
    client = providers.get_provider_client(settings.DEFAULT_PAAS_PROVIDER)
    assert client.provider_url == settings.PAAS_PROVIDERS[settings.DEFAULT_PAAS_PROVIDER]['API_URL']


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
    settings.PAAS_PROVIDERS[settings.DEFAULT_PAAS_PROVIDER]['CLIENT'] = 'not.real.class'
    with pytest.raises(providers.ProvidersImportError):
        providers.get_provider_client(settings.DEFAULT_PAAS_PROVIDER)
