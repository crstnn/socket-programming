from sock import Socket


class Server(Socket):
    def open_connection(self):
        with self.socket as s:
            s.bind((self.host, self.port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while data := conn.recv(512):
                    print(f"Received {data}")
                    conn.sendall(data)


if __name__ == '__main__':
    import configparser

    config = configparser.ConfigParser()
    config.read('host_configuration.ini')

    host = config['SERVER']['IP']
    port = int(config['SERVER']['listening_port'])

    server = Server(host, port)
    server.open_connection()
