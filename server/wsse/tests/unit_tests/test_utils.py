import pytest

from wsse.test_data import valid_wsse_headers, invalid_wsse_headers, valid_wsse_digests
from wsse.utils import parse_wsse_header, verify_wsse_digest, wsse_digest


@pytest.mark.parametrize('wsse_header,correct', valid_wsse_headers)
def test_parse_wsse_header_success(wsse_header, correct):
    username, digest, nonce, timestamp = parse_wsse_header(wsse_header)
    assert username == correct['username']
    assert digest == correct['digest']
    assert nonce == correct['nonce']
    assert timestamp == correct['timestamp']


@pytest.mark.parametrize('wsse_header', invalid_wsse_headers)
def test_parse_wsse_header_success_failure(wsse_header):
    with pytest.raises(ValueError):
        parse_wsse_header(wsse_header)


@pytest.mark.parametrize('data', valid_wsse_digests)
def test_wsse_digest(data):
    digest = wsse_digest(data['secret'], data['nonce'], data['timestamp'])
    assert digest == data['digest']


@pytest.mark.parametrize('data', valid_wsse_digests)
def test_verify_wsse_digest(data):
    assert verify_wsse_digest(data['secret'], data['nonce'], data[
                              'timestamp'], data['digest'])
