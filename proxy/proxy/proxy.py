from __future__ import absolute_import

from twisted.internet.protocol import Factory
from twisted.internet import reactor

from proxy.protocols.postgres import PostgresProtocol


class PostgresFactory(Factory):

    protocol = PostgresProtocol


reactor.listenTCP(5432, PostgresFactory())
reactor.run()
