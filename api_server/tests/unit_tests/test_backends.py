import mock
import pytest


from api_server import paas_backends
from api_server.clients.exceptions import ClientError


def test_get_backend_api_url_success(settings):
    assert paas_backends.get_backend_api_url(settings.DEFAULT_PAAS_BACKEND) == settings.PAAS_BACKENDS[
        settings.DEFAULT_PAAS_BACKEND]['API_URL']


def test_get_backend_api_url_error_mising():
    with pytest.raises(paas_backends.BackendsMissingError):
        paas_backends.get_backend_api_url('doesnotexist')


def test_get_backend_api_url_error_config(settings):
    settings.PAAS_BACKENDS['new'] = {
        'CLIENT': 'api_server.clients.base_client.BaseClient',
    }
    try:
        with pytest.raises(paas_backends.BackendsConfigError):
            paas_backends.get_backend_api_url('new')
    finally:
        settings.PAAS_BACKENDS.pop('new')


def test_get_backend_client_simple(settings):
    client = paas_backends.get_backend_client(settings.DEFAULT_PAAS_BACKEND)
    assert client.backend_url == settings.PAAS_BACKENDS[
        settings.DEFAULT_PAAS_BACKEND]['API_URL']


def test_get_backend_client_error_missing():
    with pytest.raises(paas_backends.BackendsMissingError):
        paas_backends.get_backend_client('doesnotexit')


def test_get_backend_client_error_config(settings):
    settings.PAAS_BACKENDS['new'] = {
        'API_URL': 'http://example.com',
    }
    try:
        with pytest.raises(paas_backends.BackendsConfigError):
            paas_backends.get_backend_client('new')

        settings.PAAS_BACKENDS['new'] = {
            'CLIENT': 'api_server.clients.base_client.BaseClient',
        }
        with pytest.raises(paas_backends.BackendsConfigError):
            paas_backends.get_backend_client('new')

        class DummyObject(object):

            def __init__(self, url):
                pass

        with mock.patch('api_server.paas_backends.import_string') as mocked:
            mocked.return_value = DummyObject
            with pytest.raises(paas_backends.BackendsConfigError):
                paas_backends.get_backend_client(settings.DEFAULT_PAAS_BACKEND)
    finally:
        settings.PAAS_BACKENDS.pop('new')


def test_get_backend_client_error_import(settings):
    old = settings.PAAS_BACKENDS[settings.DEFAULT_PAAS_BACKEND][
        'CLIENT']
    settings.PAAS_BACKENDS[settings.DEFAULT_PAAS_BACKEND][
        'CLIENT'] = 'not.real.class'
    try:
        with pytest.raises(paas_backends.BackendsImportError):
            paas_backends.get_backend_client(settings.DEFAULT_PAAS_BACKEND)
    finally:
        settings.PAAS_BACKENDS[settings.DEFAULT_PAAS_BACKEND]['CLIENT'] = old


@pytest.mark.django_db
def test_ensure_user_exists_success(mock_backend_client, mock_backend_authenticated_client, settings, user):
    with mock.patch('api_server.paas_backends.get_backend_client') as mocked:
        mocked.return_value = mock_backend_client
        mock_backend_client.login_or_register.return_value = (
            mock_backend_authenticated_client, True)
        result = paas_backends.get_backend_authenticated_client(
            user.username, settings.DEFAULT_PAAS_BACKEND)
    assert result == mock_backend_authenticated_client


@pytest.mark.django_db
def test_ensure_user_exists_failure_does_not_exist(settings):
    with pytest.raises(paas_backends.BackendsUserError):
        paas_backends.get_backend_authenticated_client(
            'doesnotexist', settings.DEFAULT_PAAS_BACKEND)


@pytest.mark.django_db
def test_ensure_user_exists_failure_no_backend(user):
    with pytest.raises(paas_backends.BackendsMissingError):
        paas_backends.get_backend_authenticated_client(
            user.username, 'doesnotexist')


@pytest.mark.django_db
def test_ensure_user_exists_failure_no_credentials(client, user, mock_backend_client, settings):
    with mock.patch('api_server.paas_backends.get_backend_client') as mocked:
        mocked.return_value = mock_backend_client
        with pytest.raises(paas_backends.BackendsUserError):
            paas_backends.get_backend_authenticated_client(
                user.username, 'doesnotexist')


@pytest.mark.django_db
def test_ensure_user_exists_failure_client_error(client, user, mock_backend_client, mock_backend_authenticated_client, settings):
    with mock.patch('api_server.paas_backends.get_backend_client') as mocked:
        mocked.return_value = mock_backend_client
        mock_backend_client.login_or_register.return_value = (
            mock_backend_authenticated_client, True)
        mock_backend_authenticated_client.login_or_register.side_effect = ClientError
        paas_backends.get_backend_authenticated_client(
            user.username, settings.DEFAULT_PAAS_BACKEND)
