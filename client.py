from sock import Socket


class Client(Socket):

    def send_data(self, b_str: bytes):

        with self.socket as s:
            s.connect((self.host, self.port))
            s.sendall(b_str)
            data = s.recv(512)

        print(f"Received {data!r}")


if __name__ == '__main__':
    import configparser

    config = configparser.ConfigParser()
    config.read('host_configuration.ini')

    host = config['CLIENT']['IP']
    port = int(config['CLIENT']['port'])

    client = Client(host, port)
    client.send_data(b"Hello, world")
