import mock
import pytest

from proxy.protocols.mongo import MongoProtocol


@pytest.fixture(scope='function')
def mongo_protocol(fake_transport):
    with mock.patch.object(MongoProtocol, '_connectServer'):
        p = MongoProtocol()
    p.makeConnection(fake_transport)
    return p


def test_data_received_invalid(mongo_protocol):
    data = 'insomeinvaliddata'
    mongo_protocol.dataReceived(data)

    def _check(test_data):
        assert test_data == data
    return mongo_protocol.spoof_client_queue.get().addCallback(_check)


def test_data_received_correct(mongo_protocol):
    data = '\x8e\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\xda\x07\x00\x00test\x00saslStart\x00j\x00\x00\x00\x10saslStart\x00\x01\x00\x00\x00\x02mechanism\x00\x0c\x00\x00\x00SCRAM-SHA-1\x00\x05payload\x00-\x00\x00\x00\x00n,,n=user1,r=z9+763MVWoADWsUX7RL+vzABBaftbWND\x00\x05\x00\x00\x00\x00'
    with mock.patch.object(MongoProtocol, 'connectServer'):
        mongo_protocol.dataReceived(data)
    assert mongo_protocol.hostname == 'user1'

    def _check(test_data):
        assert test_data == data
    return mongo_protocol.client_queue.get().addCallback(_check)


def test_data_received_connected(mongo_protocol):
    data = '\x8e\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\xda\x07\x00\x00test\x00saslStart\x00j\x00\x00\x00\x10saslStart\x00\x01\x00\x00\x00\x02mechanism\x00\x0c\x00\x00\x00SCRAM-SHA-1\x00\x05payload\x00-\x00\x00\x00\x00n,,n=user1,r=z9+763MVWoADWsUX7RL+vzABBaftbWND\x00\x05\x00\x00\x00\x00'
    mongo_protocol.hostname = 'hostname'
    mongo_protocol.dataReceived(data)
    assert mongo_protocol.hostname == 'hostname'

    def _check(test_data):
        assert test_data == data
    return mongo_protocol.client_queue.get().addCallback(_check)


def test_data_received_no_user(mongo_protocol, fake_transport):
    data = '\x8e\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\xda\x07\x00\x00test\x00saslStart\x00j\x00\x00\x00\x10saslStart\x00\x01\x00\x00\x00\x02mechanism\x00\x0c\x00\x00\x00SCRAM-SHA-1\x00\x05payload\x00-\x00\x00\x00\x00n,,,r=z9+763MVWoADWsUX7RL+vzABBaftbWND\x00\x05\x00\x00\x00\x00'
    mongo_protocol.dataReceived(data)
    assert mongo_protocol.hostname is None
    assert fake_transport.disconnecting is True


def test_data_received_not_scram(mongo_protocol, fake_transport):
    data = '\x8e\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\xda\x07\x00\x00test\x00saslStart\x00j\x00\x00\x00\x10saslStart\x00\x01\x00\x00\x00\x02mechanism\x00\x0c\x00\x00\x00someothermethod\x00\x05payload\x00-\x00\x00\x00\x00n,,n=user1,r=z9+763MVWoADWsUX7RL+vzABBaftbWND\x00\x05\x00\x00\x00\x00'
    mongo_protocol.dataReceived(data)
    assert mongo_protocol.hostname is None
    assert fake_transport.disconnecting is True
