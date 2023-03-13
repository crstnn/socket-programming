import socket

from host import Host


class Server(Host):
    def open_connection(self):

        with socket.socket(self.family, self.type) as s:
            s.bind((self._host, self._port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while data := conn.recv(512):
                    print(f"Received {data}")
                    conn.sendall(data)
