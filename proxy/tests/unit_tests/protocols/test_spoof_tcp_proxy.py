import mock
import pytest

from twisted.internet.defer import DeferredList

from proxy.protocols.spoof_tcp_proxy import SpoofTcpProxyProtocol


@pytest.fixture(scope='function')
def proxy_protocol(fake_transport):
    with mock.patch.object(SpoofTcpProxyProtocol, '_connectServer') as mocked:
        p = SpoofTcpProxyProtocol('spoof_host', 1234)

    mocked.assert_called_once_with(
        'spoof_host', 1234, p.spoof_server_queue, p.spoof_client_queue)
    p.makeConnection(fake_transport)
    return p


def test_send_data_spoof(proxy_protocol, fake_transport):
    data = 'testdata\ntesting123\t\n\r'
    proxy_protocol.spoof_server_queue.put(data)
    assert fake_transport.value() == data
    assert proxy_protocol.spoof_messages_length == len(data)

    proxy_protocol.spoof_server_queue.put(data)
    assert fake_transport.value() == data + data
    assert proxy_protocol.spoof_messages_length == 2 * len(data)


def test_data_received_spoof(proxy_protocol):
    data = 'testdata\ntesting123\t\n\r'
    proxy_protocol.dataReceived(data)

    def _check(test_data):
        (success1, test_data1), (success2, test_data2) = test_data
        assert success1 is True
        assert success2 is True
        assert test_data1 == data
        assert test_data2 == data

    return DeferredList([proxy_protocol.client_queue.get(), proxy_protocol.spoof_client_queue.get()]).addCallback(_check)


def test_data_received(proxy_protocol):
    data = 'testdata\ntesting123\t\n\r'
    proxy_protocol.spoof_client_queue = None
    proxy_protocol.dataReceived(data)

    def _check(test_data):
        assert test_data == data
    return proxy_protocol.client_queue.get().addCallback(_check)


def test_send_data(proxy_protocol, fake_transport):
    data = 'testdata\ntesting123\t\n\r'
    proxy_protocol.spoof_messages_length = 3
    proxy_protocol.server_queue.put(data)
    assert fake_transport.value() == data[3:]
    assert proxy_protocol.spoof_messages_length == 0

    proxy_protocol.server_queue.put(data)
    assert fake_transport.value() == data[3:] + data
    assert proxy_protocol.spoof_messages_length == 0


def test_connection_lost_spoof(proxy_protocol):
    proxy_protocol.connectionLost(None)

    def _check(test_data):
        (success1, test_data1), (success2, test_data2) = test_data
        assert success1 is True
        assert success2 is True
        assert test_data1 is False
        assert test_data2 is False

    return DeferredList([proxy_protocol.client_queue.get(), proxy_protocol.spoof_client_queue.get()]).addCallback(_check)


def test_connection_lost(proxy_protocol):
    proxy_protocol.connectionLost(None)
    proxy_protocol.spoof_client_queue = None

    def _check(data):
        assert data is False
    return proxy_protocol.client_queue.get().addCallback(_check)


def test_connect_server(proxy_protocol):
    spoof_client_queue = proxy_protocol.spoof_client_queue
    with mock.patch.object(SpoofTcpProxyProtocol, '_connectServer') as mocked:
        proxy_protocol.connectServer('localhost', 1234)
    mocked.assert_called_once_with(
        'localhost', 1234, proxy_protocol.server_queue, proxy_protocol.client_queue)
    assert proxy_protocol.spoof_server_queue is None
    assert proxy_protocol.spoof_client_queue is None

    def _check(data):
        assert data is False
    return spoof_client_queue.get().addCallback(_check)
