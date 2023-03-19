import selectors

from host import Host


class Server(Host):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.selector = selectors.DefaultSelector()

    def start(self):
        # Bind the server socket to the host and port
        self.socket.setblocking(False)
        self.socket.bind((self.host, self.port))
        # Start listening for incoming connections
        self.socket.listen()
        print(f'Server started on {self.host}:{self.port}')
        # Register the server socket with the selector.
        # Only notify the program when there is incoming data available to be read from the socket
        self.selector.register(self.socket, selectors.EVENT_READ, data=None)

        # Main event loop to handle incoming connections and data
        while True:
            events = self.selector.select(timeout=None)
            for key, event_flag in events:
                sock = key.fileobj
                if key.data is None:
                    # A new connection is being established
                    self.accept_connection(sock)
                elif event_flag & selectors.EVENT_READ:
                    # Incoming data is available to be read
                    self.handle_request(sock)

    def accept_connection(self, sock):
        # Accept the incoming connection
        client_socket, address = sock.accept()
        print(f'Connection from {address} established')
        # Register the client socket with the selector for read events
        self.selector.register(client_socket, selectors.EVENT_READ, data=self.handle_request)

    def handle_request(self, sock):
        # Receive the length header first
        length_header = sock.recv(self.length_header_buffer_size)
        if not length_header:
            # No data is received. Close connection.
            self.close_connection(sock)
            return

        length = self.message_len_from_bytes(length_header)

        chunks = []
        bytes_received = 0
        # Receive the incoming data from the socket
        while bytes_received < length:
            chunk = sock.recv(min(length - bytes_received, self.min_buffer_size))
            if not chunk:
                # No data is received. Close connection.
                self.close_connection(sock)
                return
            chunks.append(chunk)
            bytes_received += len(chunk)

        message = self.decode(b''.join(chunks))
        print(f'Received data from {sock.getpeername()}: {message}')
        self.send_message(sock, message)  # Echo the incoming data back to the client

    def close_connection(self, sock):
        print(f'Closing connection to {sock.getpeername()}')
        # Unregister the socket from the selector and close the connection
        self.selector.unregister(sock)
        sock.close()

    def close(self):
        super().close()
        self.selector.close()


if __name__ == '__main__':
    from configparser import ConfigParser

    config = ConfigParser()
    config.read('host_configuration.ini')
    server_config = config['SERVER']
    host = server_config['IP']
    port = int(server_config['listening_port'])
    server = Server(host, port)
    try:
        server.start()
    except KeyboardInterrupt:
        print("Keyboard interrupt, closing server")
        server.close()
