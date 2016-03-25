from __future__ import absolute_import

import struct

from proxy.protocols.tcp_proxy import TcpProxyProtocol


class PostgresProtocol(TcpProxyProtocol):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.hostname = None

    def dataReceived(self, data):
        if self.hostname is not None:
            super(self.__class__, self).dataReceived(data)
            return
        if len(data) < 8:
            # too short
            self.transport.loseConnection()
            return
        length, protocol = struct.unpack('!ii', data[:8])
        if length > len(data):
            self.transport.loseConnection()
            return
        if protocol == 80877103:
            # asks for SSL, for now we don't support that
            self.transport.write('N')
            return
        if protocol == 196608:
            # protocol 3.0
            values = data[8:length].strip(chr(0)).split(chr(0))
            user = None
            db_name = None
            for i in range(0, len(values), 2):
                key = values[i]
                if key == 'user':
                    user = values[i + 1]
                elif key == 'database':
                    db_name = values[i + 1]
            if db_name is not None:
                self.hostname = db_name
            elif user is not None:
                self.hostname = user
            else:
                # invalid, must at least specify user
                self.transport.loseConnection()
                return

            self.connectServer(self.hostname, 5432)
            super(self.__class__, self).dataReceived(data)
            return
        # unsupported protocol
        self.transport.loseConnection()
