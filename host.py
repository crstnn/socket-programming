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

    def send_message(self, sock, message: str):
        encoded_msg = message.encode()
        length_header = self.message_len(encoded_msg)
        sock.sendall(length_header)
        sock.sendall(encoded_msg)

    def message_len(self, message: bytes) -> bytes:
        # Length of the message as a 4-byte big-endian integer
        return len(message).to_bytes(self.length_header_buffer_size, byteorder=self.length_header_byte_order)

    def message_len_from_bytes(self, length_header: bytes) -> int:
        return int.from_bytes(length_header, byteorder=self.length_header_byte_order)

    def close(self):
        self.socket.close()
