import configparser

from server import Server

config = configparser.ConfigParser()
config.read('host_configuration.ini')

host = config['SERVER']['IP']
port = int(config['SERVER']['listening_port'])

server = Server(host, port)
server.open_connection()
