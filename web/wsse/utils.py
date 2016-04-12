import base64
import hashlib

from django.core.signing import Signer
from django.utils import crypto


def make_secret():
    return crypto.get_random_string(length=50)


def parse_wsse_header(wsse_header):
    """Take a wsse header and parses it, returning a tuple of username,
    password digest, nonce, and timestamp.

    :param str wsse_header:

    :rtype: tuple
    :returns: (username, digest, nonce, timestamp) - all str

    :raises ValueError:
        if the header is not in a valid format
    """
    try:
        username = wsse_header.split('Username="')[1].split('"')[0]
        digest = wsse_header.split('PasswordDigest="')[1].split('"')[0]
        nonce = wsse_header.split('Nonce="')[1].split('"')[0]
        timestamp = wsse_header.split('Created="')[1].split('"')[0]
    except IndexError:
        raise ValueError
    return username, digest, nonce, timestamp


def wsse_digest(secret, b64_encoded_nonce, timestamp):
    m = hashlib.sha256()
    m.update(base64.standard_b64decode(b64_encoded_nonce))
    m.update(timestamp)
    m.update(secret)
    digest = m.digest()
    return base64.standard_b64encode(digest)


def verify_wsse_digest(secret, b64_encoded_nonce, timestamp, digest, max_age=None):
    """Verify the WSSE digest, which means to check the output
    of the digest and to verify that the timestamp is within max_age.

    :param str secret:
    :param str b64_encoded_nonce:
    :param str timestamp:
    :param str digest:
    :param int max_age:
        time in seconds. Should be a nonnegative number.

    :rtype: bool
    :returns: True if the WSSE digest is valid
    """
    if max_age is not None:
        # TODO verify max age
        pass
    correct_digest = wsse_digest(secret, b64_encoded_nonce, timestamp)
    return correct_digest == digest


def get_secret(username):
    """Get the secret for this user.

    :param str username: str

    :rtype: str
    :returns: a base64 encoded string, or None if the user does not exist.
    """
    from wsse.models import WsseProfile
    try:
        profile = WsseProfile.objects.get(user__username__iexact=username)
    except WsseProfile.DoesNotExist:
        return None
    signer = Signer()
    return base64.standard_b64encode(signer.sign(profile.secret))


def regenerate_secret(username):
    from wsse.models import WsseProfile
    profile = WsseProfile.objects.get(user__username__iexact=username)
    profile.secret = make_secret()
    profile.save()
