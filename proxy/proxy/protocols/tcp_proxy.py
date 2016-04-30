from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet.protocol import Protocol


# inspired by: https://gist.github.com/fiorix/1878983

class ServerProtocol(Protocol, object):
    """The client protocol that talks to the end server in a TCP proxy.
    """

    def __init__(self, server_queue, client_queue):
        """Create a new protocol.

        :code:`server_queue` and :code:`client_queue` corresponds to the variables
        in the TCP proxy.

        :code:`self.wait_queue` is used to handle the race condition where
        :code:`self.client_queue` is ready to be consumed, but the connection has
        not been established.

        :param DeferredQueue server_queue:
        :param DeferredQueue client_queue:
        """
        self.server_queue = server_queue
        self.client_queue = client_queue
        self.wait_queue = DeferredQueue()
        self.client_queue.get().addCallback(self.clientQueueCallback)

    def clientQueueCallback(self, data):
        """A callback for the client queue.
        If the data is the literal False, then close the connection.
        Otherwise, add this data to our wait queue.

        :param data: the data from the client queue
        """
        if data is False:
            self.transport.loseConnection()
        else:
            self.wait_queue.put(data)
            self.client_queue.get().addCallback(self.clientQueueCallback)

    def emptyWaitQueue(self):
        """Starts emptying the wait queue. Note that a connection
        must already be made (self.transport must be ready for use)
        """
        def _emptyWaitQueueHelper(data):
            self.transport.write(data)
            self.wait_queue.get().addCallback(_emptyWaitQueueHelper)
        assert self.transport is not None
        self.wait_queue.get().addCallback(_emptyWaitQueueHelper)

    def connectionMade(self):
        """Connection to target server is established. Empty the wait queue.
        """
        self.emptyWaitQueue()

    def dataReceived(self, data):
        """Received data from target server, put into server queue

        :param str data:
        """
        self.server_queue.put(data)

    def connectionLost(self, why):
        """Server closed connection, or some other issue. close connection
        to server
        """
        self.server_queue.put(False)


class TcpProxyProtocol(Protocol, object):
    """A simple TCP proxy"""

    def __init__(self):
        """Create a new TCP proxy.

        `self.server_queue` contains messages from end server to client.
        `self.client_queue` contains messages from client to end server.
        """
        self.server_queue = DeferredQueue()
        self.client_queue = DeferredQueue()
        self.server_queue.get().addCallback(self.serverQueueCallback)

    def connectServer(self, hostname, port):
        """Tell the proxy what the end server is and start the connection.

        The messages in `self.client_queue` will automatically be consumed.

        This method should only be called once.

        :param str hostname:
        :param int port:
        """
        endpoint = TCP4ClientEndpoint(reactor, hostname, port)
        protocol = ServerProtocol(
            self.server_queue, self.client_queue)
        connectProtocol(endpoint, protocol)

    def serverQueueCallback(self, data):
        """A callback for `self.server_queue`

        :param str data: data from server queue
        """
        if data is False:
            self.transport.loseConnection()
            return
        self.transport.write(data)
        self.server_queue.get().addCallback(self.serverQueueCallback)

    def dataReceived(self, data):
        """Received data from client, put into client queue
        """
        self.client_queue.put(data)

    def connectionLost(self, why):
        """Client closed connection, or some other issue. close connection
        to server
        """
        self.client_queue.put(False)
