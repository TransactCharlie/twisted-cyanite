__author__ = 'charlie'

import sys
from twisted.web import server
from twisted.internet import reactor
from twisted.python import log
from http_interface.protocol import endpoints as http_endpoints

# Start the logger
log.startLogging(sys.stdout)


if __name__ == "__main__":
    # Register the HTTP Interfaces
    reactor.listenTCP(8080, server.Site(http_endpoints()), interface="0.0.0.0")

    # Register the Metrics TCP Interfaces
    # TODO: Write a Metrics TCP Interface!
    reactor.run()
