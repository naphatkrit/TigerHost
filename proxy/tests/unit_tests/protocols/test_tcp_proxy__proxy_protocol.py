import mock
import pytest

from proxy.protocols.tcp_proxy import TcpProxyProtocol


@pytest.fixture(scope='function')
def proxy_protocol(fake_transport):
    p = TcpProxyProtocol()
    p.makeConnection(fake_transport)
    return p


def test_connect_server(proxy_protocol):
    with mock.patch('proxy.protocols.tcp_proxy.connectProtocol') as mocked:
        proxy_protocol.connectServer('localhost', 1234)
    assert mocked.call_count == 1


def test_send_data(proxy_protocol, fake_transport):
    data = 'testdata\ntesting123\t\n\r'
    proxy_protocol.server_queue.put(data)
    assert fake_transport.value() == data


def test_data_received(proxy_protocol):
    data = 'testdata\ntesting123\t\n\r'
    proxy_protocol.dataReceived(data)

    def _check(test_data):
        assert test_data == data
    return proxy_protocol.client_queue.get().addCallback(_check)


def test_connection_lost(proxy_protocol):
    proxy_protocol.connectionLost(None)

    def _check(data):
        assert data is False
    return proxy_protocol.client_queue.get().addCallback(_check)
