import socket


class Client:
    def __init__(self, host, port, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print(f'Connected to server on {self.host}:{self.port}')

    def send_message(self, message):
        # Iterate over the message and send it in chunks of size equal to the buffer length
        for idx in range(0, len(message), self.buffer_size):
            chunk = message[idx:idx+self.buffer_size]
            self.client_socket.sendall(chunk.encode())
        # Receive the response from the server
        response = self.client_socket.recv(self.buffer_size)
        print(f'Received response from server: {response.decode()}')

    def close(self):
        self.client_socket.close()


if __name__ == '__main__':
    from configparser import ConfigParser
    import threading

    config = ConfigParser()
    config.read('host_configuration.ini')
    client_config = config['CLIENT']
    host = client_config['IP']
    port = int(client_config['port'])
    number_of_clients = int(client_config['number_of_clients'])

    def send_messages(client, message):
        client.connect()
        client.send_message(message)
        client.close()


    threads = []
    for i in range(number_of_clients):
        client = Client(host, port)
        message = f"Hello from client {i + 1}!"
        thread = threading.Thread(target=send_messages, args=(client, message))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
