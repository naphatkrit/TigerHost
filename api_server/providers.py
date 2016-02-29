from django.conf import settings
from django.utils.module_loading import import_string

from api_server.clients.base_client import BaseClient


class ProvidersError(Exception):
    pass


class ProvidersMissingError(ProvidersError):
    pass


class ProvidersConfigError(ProvidersError):
    pass


class ProvidersImportError(ProvidersError):
    pass


def get_provider_client(provider_name):
    """Instantiates and returns a new client for the provider

    @rtype: api_server.clients.base_client.BaseClient

    @raises: ProvidersError
    """
    if provider_name not in settings.PAAS_PROVIDERS:
        raise ProvidersMissingError
    try:
        Client = import_string(settings.PAAS_PROVIDERS[
                               provider_name]['CLIENT'])
        client = Client(settings.PAAS_PROVIDERS[provider_name]['API_URL'])
        if not isinstance(client, BaseClient):
            raise ProvidersConfigError
        return client
    except ImportError:
        raise ProvidersImportError
    except KeyError:
        raise ProvidersConfigError
