from django.conf import settings
from django.contrib.auth.models import User
from django.utils.module_loading import import_string

from api_server.clients.base_client import BaseClient
from api_server.models import Profile


class ProvidersError(Exception):
    pass


class ProvidersMissingError(ProvidersError):
    pass


class ProvidersConfigError(ProvidersError):
    pass


class ProvidersImportError(ProvidersError):
    pass


class ProvidersUserError(ProvidersError):
    pass


def get_provider_api_url(provider_name):
    """Returns the API url for this provider

    @rtype: str

    @raises e: ProvidersError
    """
    if provider_name not in settings.PAAS_PROVIDERS:
        raise ProvidersMissingError
    try:
        return settings.PAAS_PROVIDERS[provider_name]['API_URL']
    except KeyError:
        raise ProvidersConfigError


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


def get_provider_authenticated_client(username, provider):
    """Creates a new authenticated client for the user
    and provider

    @type username: str
    @type provider: str

    @rtype: api_server.clients.base_client.BaseAuthenticatedClient

    @raises e: DeisClientError
    @raises e: ProvidersError
    """
    try:
        user = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        raise ProvidersUserError('{} does not exist.'.format(username))
    client = get_provider_client(provider)
    try:
        password = user.profile.get_credential(provider).get_password()
    except Profile.NoCredentials:
        raise ProvidersUserError('{user} does not have access to {provider}.'.format(
            user=username, provider=provider))
    c, _ = client.login_or_register(
        user.username, password, user.email)
    return c
