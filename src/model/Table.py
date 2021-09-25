from typing import List

from .Card import Card
from .Player import Player


class Table:
    def __init__(self) -> None:
        self._players: List[Player] = []
        self._buy_cards: int = 0
        self._top_card: Card = None     # noqa # FIXME
        self._reverse: bool = False
        self._num_players: int = len(self._players)

    def get_players(self) -> List[Player]:
        return self._players

    def add_player(self, player: Player) -> None:
        self._players.append(player)
        return None

    def remove_player(self, player: Player) -> None:
        self._players.remove(player)
        return None

    def _next_player(self, actual_player: Player) -> Player:
        index: int = self._players.index(actual_player)
        if self._reverse:
            return self._players[index - 1]
        elif index == self._num_players - 1:
            return self._players[0]

        return self._players[index + 1]

    def is_allowed_letter(self, card: Card) -> bool:
        pass
