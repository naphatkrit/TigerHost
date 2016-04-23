from __future__ import absolute_import

from proxy.protocols.spoof_tcp_proxy import SpoofTcpProxyProtocol


class MongoProtocol(SpoofTcpProxyProtocol):

    def __init__(self):
        super(self.__class__, self).__init__('mongospoof', 27017)
        self.hostname = None

    def dataReceived(self, data):
        # couldn't find official documentation...
        # see https://github.com/mongodb/js-bson/issues/152, search for "Build command structure"
        if self.hostname is None and 'saslStart' in data:
            if 'n=' not in data or 'SCRAM-SHA-1' not in data:
                    # unsupported authentication format
                    # TODO log
                    self.transport.loseConnection()
                    return
            # TODO catch array index out of bounds error
            username = data.split('n=', 1)[1].split(',', 1)[0]
            self.hostname = username
            self.connectServer(self.hostname, 27017)
        super(self.__class__, self).dataReceived(data)
