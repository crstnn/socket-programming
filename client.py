import socket

from host import Host


class Client(Host):

    def send_data(self, b_str: bytes):

        with socket.socket(self.family, self.type) as s:
            s.connect((self._host, self._port))
            s.sendall(b_str)
            data = s.recv(512)

        print(f"Received {data!r}")
