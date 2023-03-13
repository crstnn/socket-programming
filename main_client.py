import configparser

from client import Client

config = configparser.ConfigParser()
config.read('host_configuration.ini')

host = config['CLIENT']['IP']
port = int(config['CLIENT']['port'])

client = Client(host, port)
client.send_data(b"Hello, world")
