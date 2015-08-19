__author__ = 'charlie'

from twisted.internet.protocol import Protocol, Factory
from twisted.protocols.basic import LineReceiver
from twisted.python import log
from struct import unpack, calcsize
import cPickle as pickle


class PickleProtocol(Protocol):
    # This code is lifted straight from the unpickle handles in carbon..
    # Don't blame me! - use lines instead please!!!!

    paused = False
    structFormat = "!I"
    prefixLength = calcsize(structFormat)
    MAX_LENGTH = 99999
    _unprocessed = b""
    _compatibilityOffset = 0

    def dataReceived(self, data):
        """
        Convert int prefixed strings into calls to stringReceived.
        """
        # Try to minimize string copying (via slices) by keeping one buffer
        # containing all the data we have so far and a separate offset into that
        # buffer.
        alldata = self._unprocessed + data
        currentOffset = 0
        prefixLength = self.prefixLength
        fmt = self.structFormat
        self._unprocessed = alldata

        while len(alldata) >= (currentOffset + prefixLength) and not self.paused:
            messageStart = currentOffset + prefixLength
            length, = unpack(fmt, alldata[currentOffset:messageStart])
            if length > self.MAX_LENGTH:
                self._unprocessed = alldata
                self._compatibilityOffset = currentOffset
                self.lengthLimitExceeded(length)
                return
            messageEnd = messageStart + length
            if len(alldata) < messageEnd:
                break

            # Here we have to slice the working buffer so we can send just the
            # netstring into the stringReceived callback.
            packet = alldata[messageStart:messageEnd]
            currentOffset = messageEnd
            self._compatibilityOffset = currentOffset
            self.stringReceived(packet)

            # Check to see if the backwards compat "recvd" attribute got written
            # to by application code.  If so, drop the current data buffer and
            # switch to the new buffer given by that attribute's value.
            if 'recvd' in self.__dict__:
                alldata = self.__dict__.pop('recvd')
                self._unprocessed = alldata
                self._compatibilityOffset = currentOffset = 0
                if alldata:
                    continue
                return

        # Slice off all the data that has been processed, avoiding holding onto
        # memory to store it, and update the compatibility attributes to reflect
        # that change.
        self._unprocessed = alldata[currentOffset:]
        self._compatibilityOffset = 0

    def stringReceived(self, data):
        try:
            unpickled = pickle.loads(data)

            for d in unpickled:
                log.msg(d)
                # TODO: Store metrics in backingstore!
                # TODO: Store paths in the pathstore!

        except pickle.UnpicklingError:
            log.err('invalid pickle received')



class metrics_input_pickle_factory(Factory):
    """Factory for collecting metrics from connections"""
    protocol = PickleProtocol


class LineProtocol(LineReceiver):

    delimiter = "\n"

    def lineReceived(self, line):
        log.msg(line)
        # TODO: Store metrics in backingstore!
        # TODO: Store paths in the pathstore!

class metrics_input_line_factory(Factory):
    """Factory for collecting metrics from connections"""
    protocol = LineProtocol
