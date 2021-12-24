from socket import socket, AF_INET, SOCK_STREAM
from pickle import dumps, loads
from typing import Tuple, Any

from ..view.View import View


class Client:
    def __init__(self, address: Tuple[str, int]) -> None:
        self._client: socket = socket(AF_INET, SOCK_STREAM)
        self._view: View = View()
        self._connect(address)

    def _connect(self, address: Tuple[str, int]) -> Any:
        self._client.connect(address)
        return loads(self._client.recv(2048))

    def send(self, data: Any) -> Any:
        self._client.send(dumps(data))
        return loads(self._client.recv(4096))

    def get_view(self) -> View:
        return self._view
