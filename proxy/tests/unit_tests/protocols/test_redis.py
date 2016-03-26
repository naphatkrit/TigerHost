import mock
import pytest

from proxy.protocols.redis import RedisProtocol


@pytest.fixture(scope='function')
def redis_protocol(fake_transport):
    p = RedisProtocol()
    p.makeConnection(fake_transport)
    return p


def test_get_bulk_string_input_length(redis_protocol):
    with pytest.raises(AssertionError):
        redis_protocol._getBulkString(['1', '2', '3'])


def test_get_bulk_string_not_bulk_string(redis_protocol):
    answer = redis_protocol._getBulkString(['*1', ':1000'])
    assert answer is None


def test_get_bulk_string_malformed(redis_protocol):
    answer = redis_protocol._getBulkString(['$1', 'ab'])
    assert answer is None


def test_get_bulk_string_correct(redis_protocol):
    answer = redis_protocol._getBulkString(['$2', 'ab'])
    assert answer == 'ab'


def test_data_received_connected(redis_protocol):
    data = '123'
    redis_protocol.hostname = 'db'
    redis_protocol.dataReceived(data)

    def _check(test_data):
        assert test_data == data
    return redis_protocol.client_queue.get().addCallback(_check)


@pytest.mark.parametrize('data', [
    '\r\n'.join(['1'] * 6),
    '$2\r\n$4\r\nAUTH\r\n$13\r\ntest_password\r\n',
    '*1\r\n$4\r\nAUTH\r\n$13\r\ntest_password\r\n',
    '*2\r\n$3\r\nAUTH\r\n$13\r\ntest_password\r\n',
    '*2\r\n$4\r\nAUTH\r\n$12\r\ntest_password\r\n',
    '*2\r\n$4\r\nAUTj\r\n$13\r\ntest_password\r\n',
])
def test_data_received_error(redis_protocol, fake_transport, data):
    redis_protocol.dataReceived(data)

    assert redis_protocol.hostname is None
    assert fake_transport.disconnecting is True


def test_data_received_success(redis_protocol):
    data = '*2\r\n$4\r\nAUTH\r\n$13\r\ntest_password\r\n'
    with mock.patch.object(RedisProtocol, 'connectServer') as mocked:
        redis_protocol.dataReceived(data)
    assert redis_protocol.hostname == 'test_password'
    mocked.assert_called_once_with('test_password', 6379)

    def _check(test_data):
        assert test_data == data
    return redis_protocol.client_queue.get().addCallback(_check)
