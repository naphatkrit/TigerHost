import base64
import hashlib


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
