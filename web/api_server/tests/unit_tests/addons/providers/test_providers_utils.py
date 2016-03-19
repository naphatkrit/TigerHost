import mock
import pytest

from api_server.addons.providers.base_provider import BaseAddonProvider
from api_server.addons.providers.exceptions import AddonProviderConfigError, AddonProviderImportError, AddonProviderMissingError
from api_server.addons.providers.utils import get_all_provider_names, get_provider_from_provider_name


def test_get_all_provider_names(settings):
    assert set(get_all_provider_names()) == {
        k for k in settings.ADDON_PROVIDERS}


def test_get_provider_from_provider_name_simple():
    p = get_provider_from_provider_name('test_provider')
    assert type(p) == BaseAddonProvider


def test_get_provider_from_provider_name_missing():
    with pytest.raises(AddonProviderMissingError):
        get_provider_from_provider_name('doesnotexist')


def test_get_provider_from_provider_name_config_missing(settings):
    with mock.patch.dict(settings.ADDON_PROVIDERS, {
        'test_provider': {}
    }):
        with pytest.raises(AddonProviderConfigError):
            get_provider_from_provider_name('test_provider')


def test_get_provider_from_provider_name_import(settings):
    with mock.patch.dict(settings.ADDON_PROVIDERS, {
        'test_provider': {
            'CLASS': 'doesnotexist'
        }
    }):
        with pytest.raises(AddonProviderImportError):
            get_provider_from_provider_name('test_provider')


def test_get_provider_from_provider_name_config_type(settings):
    with mock.patch.dict(settings.ADDON_PROVIDERS, {
        'test_provider': {
            'CLASS': 'api_server.addons.providers.base_provider.BaseAddonProvider',
            'ARGS': [1],
        }
    }):
        with pytest.raises(AddonProviderConfigError):
            get_provider_from_provider_name('test_provider')

    with mock.patch.dict(settings.ADDON_PROVIDERS, {
        'test_provider': {
            'CLASS': 'api_server.addons.providers.base_provider.BaseAddonProvider',
            'ARGS': 1
        }
    }):
        with pytest.raises(AddonProviderConfigError):
            get_provider_from_provider_name('test_provider')

    with mock.patch.dict(settings.ADDON_PROVIDERS, {
        'test_provider': {
            'CLASS': 'api_server.addons.providers.base_provider.BaseAddonProvider',
            'KWARGS': {'test': '123'}
        }
    }):
        with pytest.raises(AddonProviderConfigError):
            get_provider_from_provider_name('test_provider')

    with mock.patch.dict(settings.ADDON_PROVIDERS, {
        'test_provider': {
            'CLASS': 'api_server.addons.providers.base_provider.BaseAddonProvider',
            'KWARGS': 1
        }
    }):
        with pytest.raises(AddonProviderConfigError):
            get_provider_from_provider_name('test_provider')
