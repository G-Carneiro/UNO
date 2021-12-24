from socket import socket, AF_INET, SOCK_STREAM
from pickle import dumps, loads

from .Server import Server
from .Client import Client


class Network:
    def __init__(self, server: Server = Server()) -> None:
        self._server: Server = server
        self._client: Client = Client(self._server.get_address())

    def send(self, data):
        return self._client.send(data=data)
