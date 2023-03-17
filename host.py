import selectors

from abc import ABC as ABSTRACT
import socket


class Host(ABSTRACT):
    def __init__(self, host, port,
                 family=socket.AF_INET,
                 socket_type=socket.SOCK_STREAM  # protocol: TCP (note use socket.SOCK_DGRAM for UDP)
                 ):
        self.host = host
        self.port = port
        self.family = family
        self.type = socket_type
        self.buffer_size = 1024
        self.socket = socket.socket(self.family, self.type)
        self.selector = selectors.DefaultSelector()

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(self.buffer_size)  # Should be ready to read
            if recv_data:
                data.out_bytes += recv_data
            else:
                print(f"Closing connection to {data.id}")
                self.selector.unregister(sock)
                sock.close()
        if (mask & selectors.EVENT_WRITE) and data.out_bytes:
            print(f"Echoing {data.out_bytes!r} to {data.id}")
            sent = sock.send(data.out_bytes)  # Should be ready to write
            data.out_bytes = data.out_bytes[sent:]
        return sock, data

    def close(self):
        self.selector.close()
