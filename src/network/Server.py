from socket import socket, AF_INET, SOCK_STREAM, gethostname


class Server:
    def __init__(self, port: int = 5555, connection_limit: int = 10) -> None:
        self._port: int = port

        host = gethostname()
        self._server_socket: socket = socket(AF_INET, SOCK_STREAM)
        self._server_socket.bind((host, port))
        self._server_socket.listen(connection_limit)
