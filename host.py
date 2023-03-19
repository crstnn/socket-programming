import selectors

from abc import ABC as ABSTRACT
import socket


class Host(ABSTRACT):
    def __init__(self, host, port,
                 min_buffer_size=1024,
                 family=socket.AF_INET,
                 socket_type=socket.SOCK_STREAM  # protocol: TCP (note use socket.SOCK_DGRAM for UDP)
                 ):
        self.host = host
        self.port = port
        self.family = family
        self.type = socket_type
        self.length_header_buffer_size = 4
        self.length_header_byte_order = 'big'  # big-endian
        self.min_buffer_size = min_buffer_size
        self.socket = socket.socket(self.family, self.type)
        self.selector = selectors.DefaultSelector()

    def send_message(self, sock, message: bytes):
        length_header = self.get_message_len(message)
        sock.sendall(length_header)
        sock.sendall(message)

    def get_message_len(self, message) -> bytes:
        # Length of the message as a 4-byte big-endian integer
        return len(message).to_bytes(self.length_header_buffer_size,
                                     byteorder=self.length_header_byte_order)

    def get_message_len_from_bytes(self, length_header: bytes) -> int:
        return int.from_bytes(length_header,
                              byteorder=self.length_header_byte_order)

    def close(self):
        self.socket.close()
        self.selector.close()
