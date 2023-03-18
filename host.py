import selectors

from abc import ABC as ABSTRACT
import socket


class Host(ABSTRACT):
    def __init__(self, host, port,
                 buffer_size=1024,
                 family=socket.AF_INET,
                 socket_type=socket.SOCK_STREAM  # protocol: TCP (note use socket.SOCK_DGRAM for UDP)
                 ):
        self.host = host
        self.port = port
        self.family = family
        self.type = socket_type
        self.buffer_size = buffer_size
        self.socket = socket.socket(self.family, self.type)
        self.selector = selectors.DefaultSelector()

    def close(self):
        self.selector.close()
