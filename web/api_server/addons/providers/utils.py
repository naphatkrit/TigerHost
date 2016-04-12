from django.conf import settings
from django.utils.module_loading import import_string

from api_server.addons.providers.exceptions import AddonProviderConfigError, AddonProviderImportError, AddonProviderMissingError


def get_all_provider_names():
    """Get the list of all addon providers installed on this system.

    :rtype: list
    :return: list of providers (str)
    """
    return settings.ADDON_PROVIDERS.keys()


def get_provider_from_provider_name(provider_name):
    """Given the name of a provider, return the provider object.

    :param str provider_name: the name of the addons provider

    :rtype: api_server.addons.providers.base_provider.BaseAddonProvider

    :raises api_server.addons.providers.exceptions.AddonProviderMissingError:
    :raises api_server.addons.providers.exceptions.AddonProviderConfigError:
    """
    if provider_name not in settings.ADDON_PROVIDERS:
        raise AddonProviderMissingError(
            '{} does not exist.'.format(provider_name))
    config = settings.ADDON_PROVIDERS[provider_name]
    if 'CLASS' not in config:
        raise AddonProviderConfigError(
            '{} is improperly configured. The key "CLASS" is missing.'.format(provider_name))
    try:
        Provider = import_string(config['CLASS'])
    except ImportError:
        raise AddonProviderImportError(
            'Class path {} cannot be imported for provider {}.'.format(config['CLASS'], provider_name))
    args = config.get('ARGS', tuple())
    kwargs = config.get('KWARGS', dict())
    try:
        return Provider(*args, **kwargs)
    except TypeError:
        raise AddonProviderConfigError('{} is improperly configured. Class {} does not take the given positional and keyword arguments.'.format(provider_name, config['CLASS']))
