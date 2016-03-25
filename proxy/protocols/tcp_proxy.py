from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet.protocol import Protocol


# inspired by: https://gist.github.com/fiorix/1878983

class ServerProtocol(Protocol, object):

    def __init__(self, server_queue, client_queue):
        self.server_queue = server_queue
        self.client_queue = client_queue
        self.wait_queue = DeferredQueue()
        self.client_queue.get().addCallback(self.clientQueueCallback)

    def clientQueueCallback(self, data):
        if data is False:
            self.transport.loseConnection()
        else:
            self.wait_queue.put(data)
            self.client_queue.get().addCallback(self.clientQueueCallback)

    def emptyWaitQueue(self):
        def _emptyWaitQueueHelper(data):
            self.transport.write(data)
            self.wait_queue.get().addCallback(_emptyWaitQueueHelper)
        assert self.transport is not None
        self.wait_queue.get().addCallback(_emptyWaitQueueHelper)

    def connectionMade(self):
        self.emptyWaitQueue()

    def dataReceived(self, data):
        self.server_queue.put(data)


class TcpProxyProtocol(Protocol, object):

    def __init__(self):
        self.server_queue = DeferredQueue()
        self.client_queue = DeferredQueue()
        self.server_queue.get().addCallback(self.serverQueueCallback)

    def connectServer(self, hostname, port):
        endpoint = TCP4ClientEndpoint(reactor, hostname, port)
        protocol = ServerProtocol(
            self.server_queue, self.client_queue)
        connectProtocol(endpoint, protocol)

    def serverQueueCallback(self, data):
        self.transport.write(data)
        self.server_queue.get().addCallback(self.serverQueueCallback)

    def dataReceived(self, data):
        self.client_queue.put(data)

    def connectionLost(self, why):
        # TODO pretty sure this only allows client to close connection, not the
        # other way around
        self.client_queue.put(False)
