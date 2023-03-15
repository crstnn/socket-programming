from abc import ABC as ABSTRACT
import socket


class Socket(ABSTRACT):

    def __init__(self, host, port,
                 family=socket.AF_INET,
                 socket_type=socket.SOCK_STREAM  # protocol: TCP (note use socket.SOCK_DGRAM for UDP)
                 ):
        self.host = host
        self.port = port
        self.family = family
        self.type = socket_type
        self.socket = socket.socket(self.type, self.type)

    def new_socket(self):
        self.socket = socket.socket(self.type, self.type)
