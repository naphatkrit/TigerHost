import base64
import hashlib

from django.core.signing import Signer

from wsse.models import WsseProfile


def parse_wsse_header(wsse_header):
    """Take a wsse header and parses it, returning a tuple of username,
    password digest, nonce, and timestamp.

    @type wsse_header: str

    @rtype: tuple
        (username, digest, nonce, timestamp) - all str

    @raises e: ValueError
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


def wsse_digest(secret, nonce, timestamp):
    m = hashlib.sha1()
    m.update(nonce)
    m.update(timestamp)
    m.update(secret)
    digest = m.digest()
    return base64.standard_b64encode(digest)


def verify_wsse_digest(secret, nonce, timestamp, digest, max_age=None):
    """Verify the WSSE digest, which means to check the output
    of the digest and to verify that the timestamp is within max_age.

    @type secret: str

    @type nonce: str

    @type timestamp: str

    @type digest: str

    @type max_age: int
        time in seconds. Should be a nonnegative number.

    @rtype: bool
        True if the WSSE digest is valid
    """
    if max_age is not None:
        # TODO verify max age
        pass
    correct_digest = wsse_digest(secret, nonce, timestamp)
    return correct_digest == digest


def get_secret(username):
    """Get the secret for this user.

    @type username: str

    @rtype: str
        returns a base64 encoded string. Returns None if the user does not exist.
    """
    try:
        profile = WsseProfile.objects.get(user__username__iexact=username)
    except WsseProfile.DoesNotExist:
        return None
    signer = Signer()
    return base64.standard_b64encode(signer.sign(profile.secret.bytes))
