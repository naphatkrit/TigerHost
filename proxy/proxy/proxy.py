from __future__ import absolute_import

from twisted.internet.protocol import Factory
from twisted.internet import reactor

from proxy.protocols.postgres import PostgresProtocol
from proxy.protocols.redis import RedisProtocol


class PostgresFactory(Factory):

    protocol = PostgresProtocol


class RedisFactory(Factory):

    protocol = RedisProtocol


def main():
    reactor.listenTCP(5432, PostgresFactory())
    reactor.listenTCP(6379, RedisFactory())
    reactor.run()
