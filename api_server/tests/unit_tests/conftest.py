import base64
import datetime
import mock
import pytest

from django.contrib.auth.models import User
from django.utils import crypto

from api_server.clients.base_client import BaseClient
from api_server.clients.base_authenticated_client import BaseAuthenticatedClient
from api_server.models import App
from wsse.utils import get_secret, wsse_digest


@pytest.fixture(scope='function')
def username():
    return crypto.get_random_string()


@pytest.fixture(scope='function')
def email(username):
    return '{}@princeton.edu'.format(username)


@pytest.fixture(scope='function')
def password():
    return crypto.get_random_string()


@pytest.fixture(scope='function')
def user(username, email):
    return User.objects.create_user(username, email=email)


@pytest.fixture(scope='function')
def username2():
    return crypto.get_random_string()


@pytest.fixture(scope='function')
def email2(username2):
    return '{}@princeton.edu'.format(username2)


@pytest.fixture(scope='function')
def password2():
    return crypto.get_random_string()


@pytest.fixture(scope='function')
def user2(username2, email2):
    return User.objects.create_user(username2, email=email2)


@pytest.fixture(scope='function')
def api_key(user):
    return get_secret(user.username)  # uses user fixture so user is created


@pytest.fixture(scope='function')
def wsse_header(api_key, username):
    nonce = base64.standard_b64encode(crypto.get_random_string())
    timestamp = datetime.datetime.utcnow()
    timestamp_str = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    digest = wsse_digest(api_key, nonce, timestamp_str)
    return '''UsernameToken Username="{username}", PasswordDigest="{digest}", Nonce="{nonce}", Created="{timestamp}"'''.format(
        username=username, digest=digest, nonce=nonce, timestamp=timestamp_str)


@pytest.fixture(scope='function')
def http_headers(wsse_header):
    return {
        'HTTP_AUTHORIZATION': 'WSSE profile="UsernameToken"',
        'HTTP_X_WSSE': wsse_header,
    }


@pytest.fixture
def mock_provider_authenticated_client():
    mocked = mock.Mock(spec=BaseAuthenticatedClient)
    return mocked


@pytest.fixture
def mock_provider_client():
    return mock.Mock(spec=BaseClient)


@pytest.fixture(scope='function')
def app_id():
    return crypto.get_random_string(allowed_chars='abcdefghijklmnopqrstuvwxyz1234567890-')


@pytest.fixture(scope='function')
def make_app(app_id, settings):
    App.objects.create(app_id=app_id, provider_name=settings.DEFAULT_PAAS_PROVIDER)
