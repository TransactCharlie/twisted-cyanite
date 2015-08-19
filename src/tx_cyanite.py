__author__ = 'charlie'

import sys
from twisted.web import server
from twisted.internet import reactor
from twisted.python import log
from http_interface.protocols import endpoints as http_endpoints
from metrics_interface.protocols import metrics_input_pickle_factory, metrics_input_line_factory

# Start the logger
log.startLogging(sys.stdout)


if __name__ == "__main__":
    # Register the HTTP Interfaces
    reactor.listenTCP(8080, server.Site(http_endpoints()), interface="0.0.0.0")

    # Register the Metrics TCP Interfaces
    reactor.listenTCP(2003, metrics_input_line_factory())
    reactor.listenTCP(2004, metrics_input_pickle_factory())

    # Start
    reactor.run()
