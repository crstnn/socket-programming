import socket
from abc import ABC as ABSTRACT


class Host(ABSTRACT):
    def __init__(self, host, port,
                 family=socket.AF_INET,
                 socket_type=socket.SOCK_STREAM  # protocol: TCP (note use socket.SOCK_DGRAM for UDP)
                 ):
        self.host = host
        self.port = port
        self.family = family
        self.type = socket_type
        self.length_header_buffer_size = 4
        self.length_header_byte_order = 'big'  # big-endian
        self.max_buffer_size = 1024
        self.encoding = 'UTF-8'
        self.socket = socket.socket(self.family, self.type)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def send_message(self, sock, message: str):
        encoded_msg = self.encode(message)
        length_header = self.message_len(encoded_msg)
        sock.sendall(length_header)
        sock.sendall(encoded_msg)

    def receive_message(self, sock) -> str | None:
        # Receive the length header first
        length_header = sock.recv(self.length_header_buffer_size)
        if not length_header:
            # No data is received. Close connection.
            self.close_connection(sock)
            return

        msg_length = self.message_len_from_bytes(length_header)

        chunks = []
        bytes_received = 0
        # Receive the incoming (variable length) data from the socket
        while bytes_received < msg_length:
            chunk = sock.recv(min(msg_length - bytes_received, self.max_buffer_size))
            if not chunk:
                # No data is received. Close connection.
                self.close_connection(sock)
                return
            chunks.append(chunk)
            bytes_received += len(chunk)

        return self.decode(b''.join(chunks))

    def close_connection(self, sock):
        print(f'Closing connection to {sock.getpeername()}')
        sock.close()

    def encode(self, message: str):
        return message.encode(self.encoding)

    def decode(self, message: bytes):
        return message.decode(self.encoding)

    def message_len(self, message: bytes) -> bytes:
        # Length of the message as a 4-byte big-endian integer
        return len(message).to_bytes(self.length_header_buffer_size, byteorder=self.length_header_byte_order)

    def message_len_from_bytes(self, length_header: bytes) -> int:
        return int.from_bytes(length_header, byteorder=self.length_header_byte_order)

    def close(self):
        self.socket.close()
