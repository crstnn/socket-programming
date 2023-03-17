import socket
import selectors


class Server:
    def __init__(self, host, port, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.selector = selectors.DefaultSelector()

    def start(self):
        # Bind the server socket to the host and port
        self.server_socket.bind((self.host, self.port))
        # Start listening for incoming connections
        self.server_socket.listen()
        print(f'Server started on {self.host}:{self.port}')

        # Register the server socket with the selector for read events
        self.selector.register(self.server_socket, selectors.EVENT_READ, data=None)

        # Start the main event loop to handle incoming connections and data
        while True:
            events = self.selector.select()
            for key, mask in events:
                if key.data is None:
                    # A new connection is being established
                    self.accept_connection(key.fileobj)
                elif mask & selectors.EVENT_READ:
                    # Incoming data is available to be read
                    self.handle_request(key.fileobj)

    def accept_connection(self, sock):
        # Accept the incoming connection
        client_socket, address = sock.accept()
        print(f'Connection from {address} established')
        # Register the client socket with the selector for read events
        self.selector.register(client_socket, selectors.EVENT_READ, data=self.handle_request)

    def handle_request(self, sock):
        # Receive incoming data from the socket
        data = sock.recv(self.buffer_size)
        if data:
            print(f'Received data from {sock.getpeername()}: {data.decode()}')
            # Echo the incoming data back to the client
            sock.sendall(data)
        else:
            # If no data is received, the connection is closed
            print(f'Closing connection to {sock.getpeername()}')
            # Unregister the socket from the selector and close the connection
            self.selector.unregister(sock)
            sock.close()

    def close(self):
        self.selector.close()
        self.server_socket.close()


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
