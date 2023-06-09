from host import Host


class Client(Host):

    def connect(self):
        self.socket.connect((self.host, self.port))
        print(f'Connected to server on {self.host}:{self.port}')

    def send_echo_message(self, message: str):
        self.send_message(self.socket, message)
        response = self.receive_message(self.socket)
        print(f'Received response from server: {response}')


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
        client.send_echo_message(message)
        client.close()


    # Simulate multiple clients talking to one server
    threads = []
    for i in range(number_of_clients):
        client = Client(host, port)
        message = f"Hello from client {i + 1}! {'test' * 20000} final"
        thread = threading.Thread(target=send_messages, args=(client, message))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
