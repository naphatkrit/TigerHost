import struct
import mock
import pytest

from proxy.protocols.postgres import PostgresProtocol


@pytest.fixture(scope='function')
def postgres_protocol(fake_transport):
    p = PostgresProtocol()
    p.makeConnection(fake_transport)
    return p


def test_data_received_connected(postgres_protocol):
    data = '123'
    postgres_protocol.hostname = 'db'
    postgres_protocol.dataReceived(data)

    def _check(test_data):
        assert test_data == data
    return postgres_protocol.client_queue.get().addCallback(_check)


def test_data_received_length(postgres_protocol, fake_transport):
    data = '1234567'
    postgres_protocol.dataReceived(data)
    assert postgres_protocol.hostname is None
    assert fake_transport.disconnecting is True


def test_data_received_invalid_length(postgres_protocol, fake_transport):
    data = struct.pack('!ii', 9, 196608)
    postgres_protocol.dataReceived(data)
    assert postgres_protocol.hostname is None
    assert fake_transport.disconnecting is True


def test_data_received_ssl(postgres_protocol, fake_transport):
    data = struct.pack('!ihh', 8, 1234, 5679)
    postgres_protocol.dataReceived(data)
    assert postgres_protocol.hostname is None
    assert fake_transport.value() == 'N'


def test_data_received_invalid_protocol(postgres_protocol, fake_transport):
    data = struct.pack('!ihh', 8, 4, 0)
    postgres_protocol.dataReceived(data)
    assert postgres_protocol.hostname is None
    assert fake_transport.disconnecting is True


def test_data_received_no_db(postgres_protocol, fake_transport):
    data = struct.pack('!ihh4sb9sbb', 8 + 4 + 1 + 9 + 1 + 1,
                       3, 0, 'user', 0, 'test_user', 0, 0)
    with mock.patch.object(PostgresProtocol, 'connectServer') as mocked:
        postgres_protocol.dataReceived(data)
    assert postgres_protocol.hostname == 'test_user'
    mocked.assert_called_once_with('test_user', 5432)

    def _check(test_data):
        assert test_data == data
    return postgres_protocol.client_queue.get().addCallback(_check)


def test_data_received_no_hostname(postgres_protocol, fake_transport):
    data = struct.pack('!ihh4sb9sb8sb2sbb', 8 + 4 + 1 + 9 + 1 + 8 + 1 +
                       2 + 1 + 1, 3, 0, 'usef', 0, 'test_user', 0, 'databasf', 0, 'db', 0, 0)
    postgres_protocol.dataReceived(data)
    assert postgres_protocol.hostname is None
    assert fake_transport.disconnecting is True
