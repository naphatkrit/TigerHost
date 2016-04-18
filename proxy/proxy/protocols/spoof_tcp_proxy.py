from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol

from proxy.protocols.tcp_proxy import ServerProtocol


class SpoofTcpProxyProtocol(Protocol, object):
    """This is a special kind of TCP proxy where the connection
    is initially routed to a spoof server, and then when
    identifying information is sent from the client,
    the connection is made to the right server and
    messages are relayed.

    This assumes that the spoof server and the real server
    gives the exact same response up to the time the real
    server is connected to.
    """

    def __init__(self, spoof_hostname, spoof_port):
        """Create a new spoof TCP proxy.

        :param str spoof_hostname: the hostname of the spoof server
        :param int spoof_port: the port of the spoof server
        """
        # how many bytes have been sent by the spoof server?
        self.spoof_messages_length = 0

        # for the actual server connection
        self.server_queue = DeferredQueue()
        self.client_queue = DeferredQueue()

        # for the spoofed connection
        self.spoof_client_queue = DeferredQueue()
        self.spoof_server_queue = DeferredQueue()
        self._connectServer(spoof_hostname, spoof_port,
                            self.spoof_server_queue, self.spoof_client_queue)

        # add callbacks
        self.server_queue.get().addCallback(self.serverQueueCallback)
        self.spoof_server_queue.get().addCallback(self.spoofServerQueueCallback)

    def serverQueueCallback(self, data):
        """A callback for `self.server_queue`

        This only starts sending data after
        :code:`spoof_messages_length` has gone to 0. If the
        incoming data is longer than
        :code:`spoof_messages_length`, then that many bytes is
        truncated from the beginning and the rest is sent.

        :param str data: data from server queue
        """
        assert self.spoof_messages_length >= 0
        if self.spoof_messages_length == 0:
            self.transport.write(data)
        else:
            if self.spoof_messages_length < len(data):
                data = data[self.spoof_messages_length:]
                self.spoof_messages_length = 0
                self.transport.write(data)
            else:
                self.spoof_messages_length -= len(data)
        self.server_queue.get().addCallback(self.serverQueueCallback)

    def spoofServerQueueCallback(self, data):
        """A callback for `self.spoof_server_queue`

        :param str data: data from server queue
        """
        if self.spoof_server_queue is not None:
            self.spoof_messages_length += len(data)
            self.transport.write(data)
            self.spoof_server_queue.get().addCallback(self.spoofServerQueueCallback)

    def _connectServer(self, hostname, port, server_queue, client_queue):
        """A helper function for connecting to (hostname, port)
        with the given server and client queues.

        :param str hostname:
        :param int port:
        :param DeferredQueue server_queue:
        :param DeferredQueue client_queue:
        """
        endpoint = TCP4ClientEndpoint(reactor, hostname, port)
        protocol = ServerProtocol(
            server_queue, client_queue)
        connectProtocol(endpoint, protocol)

    def connectServer(self, hostname, port):
        """Tell the proxy what the end server is and start the connection. This closes the connection to the spoofed
        server.

        :param str hostname:
        :param int port:
        :param DeferredQueue server_queue:
        :param DeferredQueue client_queue:
        """
        # close connection
        self.spoof_client_queue.put(False)
        self.spoof_client_queue = None
        self.spoof_server_queue = None

        self._connectServer(
            hostname, port, self.server_queue, self.client_queue)

    def dataReceived(self, data):
        """Received data from client, put into client queue
        """
        self.client_queue.put(data)
        if self.spoof_client_queue is not None:
            self.spoof_client_queue.put(data)

    def connectionLost(self, why):
        """Client closed connection, or some other issue. close connection
        to server
        """
        # TODO pretty sure this only allows client to close connection, not the
        # other way around
        self.client_queue.put(False)
        if self.spoof_client_queue is not None:
            self.spoof_client_queue.put(False)
