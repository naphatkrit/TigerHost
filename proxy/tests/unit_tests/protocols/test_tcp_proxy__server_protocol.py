import pytest

from twisted.internet.defer import DeferredQueue

from proxy.protocols.tcp_proxy import ServerProtocol


@pytest.fixture(scope='function')
def client_queue():
    return DeferredQueue()


@pytest.fixture(scope='function')
def server_queue():
    return DeferredQueue()


@pytest.fixture(scope='function')
def server_protocol(fake_transport, server_queue, client_queue):
    p = ServerProtocol(server_queue, client_queue)
    p.makeConnection(fake_transport)
    return p


def test_send_data(server_protocol, client_queue, fake_transport):
    data = 'testdata\ntesting123\t\n\r'
    client_queue.put(data)
    assert fake_transport.value() == data


def test_send_data_buffered(server_queue, client_queue, fake_transport):
    p = ServerProtocol(server_queue, client_queue)

    client_queue.put('1')
    client_queue.put('2')

    p.makeConnection(fake_transport)
    assert fake_transport.value() == '12'

    client_queue.put('3')
    assert fake_transport.value() == '123'


def test_receive_data(server_protocol, server_queue):
    data = '123'
    server_protocol.dataReceived(data)

    def _check(test_data):
        assert test_data == data
    return server_queue.get().addCallback(_check)


def test_close_connection(server_protocol, client_queue, fake_transport):
    client_queue.put(False)
    assert fake_transport.disconnecting is True
