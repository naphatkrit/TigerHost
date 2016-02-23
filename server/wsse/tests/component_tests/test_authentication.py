import pytest

from datetime import datetime
from django.contrib.auth.models import User
from django.utils import crypto

from wsse.utils import get_secret, wsse_digest


@pytest.mark.django_db
def test_success(client, username, password, email):
    User.objects.create_user(username, email, password)
    secret = get_secret(username)
    nonce = crypto.get_random_string()
    timestamp = datetime.utcnow().isoformat()
    digest = wsse_digest(secret, nonce, timestamp)
    wsse_header = '''UsernameToken Username="{username}", PasswordDigest="{digest}", Nonce="{nonce}", Created="{timestamp}"'''.format(
        username=username, digest=digest, nonce=nonce, timestamp=timestamp)
    resp = client.get('/wsse_test/', HTTP_AUTHORIZATION='WSSE profile="UsernameToken"', HTTP_X_WSSE=wsse_header)
    assert resp.status_code == 200
    assert resp.content == username


def test_failure(client):
    resp = client.get('/wsse_test/')
    assert resp.status_code == 401
