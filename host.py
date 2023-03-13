from abc import ABC as ABSTRACT
import socket


class Host(ABSTRACT):

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self.family = socket.AF_INET
        self.type = socket.SOCK_STREAM  # protocol: TCP (note use socket.SOCK_DGRAM for UDP)
