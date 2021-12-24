from socket import socket, AF_INET, SOCK_STREAM, gethostname
from pickle import dumps, loads
from _thread import start_new_thread
from typing import Tuple


class Server:
    def __init__(self, port: int = 5555, connection_limit: int = 10) -> None:
        self._port: int = port
        self._host: str = gethostname()
        self._address: Tuple[str, int] = (self._host, self._port)
        self._server_socket: socket = socket(AF_INET, SOCK_STREAM)
        self._server_socket.bind(self._address)
        self._server_socket.listen(connection_limit)

    def get_address(self) -> Tuple[str, int]:
        return self._address

    def get_port(self) -> int:
        return self._port

    def get_host(self) -> str:
        return self._host

    def thread_client(self, connection: socket) -> None:
        while True:
            data = loads(connection.recv(4096))
            if (not data):
                break

        connection.close()
        return None

    def run(self) -> None:
        while True:
            client_connection, client_address = self._server_socket.accept()

            start_new_thread(self.thread_client, ())
