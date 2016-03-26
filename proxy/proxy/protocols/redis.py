from __future__ import absolute_import

from proxy.protocols.tcp_proxy import TcpProxyProtocol


class RedisProtocol(TcpProxyProtocol):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.hostname = None

    def _getBulkString(self, tokens):
        """Take a tokens array of length 2, return the bulk string
        represented by the array. Returns None on error.

        @type tokens: list
            list of strings

        @rtype: str
            The bulk string, or None in case of an error
        """
        assert len(tokens) == 2
        if tokens[0][0] != '$':
            # not a bulk string
            return None
        length = int(tokens[0][1:])
        body = tokens[1]
        if len(body) != length:
            # malformed string
            return None
        return body

    def dataReceived(self, data):
        """Implement a redis proxy.

        The url redis://:password@host:port/db_num is mapped to:
        redis://:password@password:6379/db_num

        That is, the password is used as the host, and the port number
        is fixed to 6379
        """
        # see http://redis.io/topics/protocol
        if self.hostname is not None:
            super(self.__class__, self).dataReceived(data)
            return
        # NOTE this doesn't allow bulk strings to contain \r\n,
        # but that's ok for our use case
        values = data.strip('\r\n').split('\r\n')
        if len(values) != 5:
            self.transport.loseConnection()
            return
        if values[0][0] != '*' or values[0][1] != '2':
            # we only take an array of length 2
            self.transport.loseConnection()
            return
        action = self._getBulkString(values[1:3])
        if action != 'AUTH':
            self.transport.loseConnection()
            return
        password = self._getBulkString(values[3:5])
        if password is None:
            self.transport.loseConnection()
            return
        self.hostname = password
        self.connectServer(self.hostname, 6379)
        super(self.__class__, self).dataReceived(data)
