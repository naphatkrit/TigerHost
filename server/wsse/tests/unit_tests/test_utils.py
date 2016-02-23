import pytest

from wsse.utils import parse_wsse_header, wsse_digest


_wsse_header = '''UsernameToken Username="bob", PasswordDigest="quR/EWLAV4xLf9Zqyw4pDmfV9OY=", Nonce="d36e316282959a9ed4c89851497a717f", Created="2003-12-15T14:43:07Z"'''


def test_parse_wsse_header_success():
    username, digest, nonce, timestamp = parse_wsse_header(_wsse_header)
    assert username == 'bob'
    assert digest == 'quR/EWLAV4xLf9Zqyw4pDmfV9OY='
    assert nonce == 'd36e316282959a9ed4c89851497a717f'
    assert timestamp == '2003-12-15T14:43:07Z'


@pytest.mark.parametrize('wsse_header', [
    '''UsernameToken PasswordDigest="quR/EWLAV4xLf9Zqyw4pDmfV9OY=", Nonce="d36e316282959a9ed4c89851497a717f", Created="2003-12-15T14:43:07Z"''',

    '''UsernameToken Username="bob", Nonce="d36e316282959a9ed4c89851497a717f", Created="2003-12-15T14:43:07Z"''',

    '''UsernameToken Username="bob", PasswordDigest="quR/EWLAV4xLf9Zqyw4pDmfV9OY=", Created="2003-12-15T14:43:07Z"''',

    '''UsernameToken Username="bob", PasswordDigest="quR/EWLAV4xLf9Zqyw4pDmfV9OY=", Nonce="d36e316282959a9ed4c89851497a717f"'''
])
def test_parse_wsse_header_success_failure(wsse_header):
    with pytest.raises(ValueError):
        parse_wsse_header(wsse_header)


@pytest.mark.parametrize('secret,nonce,timestamp,correct', [
    ('taadtaadpstcsm', 'd36e316282959a9ed4c89851497a717f',
     '2003-12-15T14:43:07Z', 'quR/EWLAV4xLf9Zqyw4pDmfV9OY=')
])
def test_wsse_digest(secret, nonce, timestamp, correct):
    digest = wsse_digest(secret, nonce, timestamp)
    assert digest == correct
