from django.conf import settings
from django.contrib.auth.models import User
from django.utils.module_loading import import_string

from api_server.clients.base_client import BaseClient
from api_server.models import Profile


class BackendsError(Exception):
    pass


class BackendsMissingError(BackendsError):
    pass


class BackendsConfigError(BackendsError):
    pass


class BackendsImportError(BackendsError):
    pass


class BackendsUserError(BackendsError):
    pass


def get_backend_api_url(backend):
    """Returns the API url for this backend

    :param str backend: the backend name

    :rtype: str
    :returns: the backend URL

    @raises e: BackendsError
    """
    if backend not in settings.PAAS_BACKENDS:
        raise BackendsMissingError
    try:
        return settings.PAAS_BACKENDS[backend]['API_URL']
    except KeyError:
        raise BackendsConfigError


def get_backend_client(backend):
    """Instantiates and returns a new client for the backend

    @rtype: api_server.clients.base_client.BaseClient

    @raises: BackendsError
    """
    if backend not in settings.PAAS_BACKENDS:
        raise BackendsMissingError
    try:
        Client = import_string(settings.PAAS_BACKENDS[
                               backend]['CLIENT'])
        client = Client(settings.PAAS_BACKENDS[backend]['API_URL'])
        if not isinstance(client, BaseClient):
            raise BackendsConfigError
        return client
    except ImportError:
        raise BackendsImportError
    except KeyError:
        raise BackendsConfigError


def get_backend_authenticated_client(username, backend):
    """Creates a new authenticated client for the user
    and backend

    @type username: str
    @type backend: str

    @rtype: api_server.clients.base_client.BaseAuthenticatedClient

    @raises e: ClientError
    @raises e: BackendsError
    """
    try:
        user = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        raise BackendsUserError('{} does not exist.'.format(username))
    client = get_backend_client(backend)
    try:
        password = user.profile.get_credential(backend).get_password()
    except Profile.NoCredentials:
        raise BackendsUserError('{user} does not have access to {backend}.'.format(
            user=username, backend=backend))
    c, _ = client.login_or_register(
        user.username, password, user.email)
    return c
