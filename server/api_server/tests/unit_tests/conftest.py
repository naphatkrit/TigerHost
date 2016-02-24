import base64
import datetime
import pytest

from django.contrib.auth.models import User
from django.utils import crypto

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
