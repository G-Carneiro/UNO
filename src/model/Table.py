from typing import List, Dict

from .Card import Card
from .Color import Color
from .Player import Player


class Table:
    def __init__(self) -> None:
        self._players: List[Player] = []
        self._value_to_buy: int = 0
        self._deck: Dict[List[Card]] = {}   # FIXME: keys
        self._top_card: Card = None         # FIXME: type
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

    def _set_deck(self) -> None:
        for color in Color:
            for value in range(10):
                card = Card(value=value, color=color)
                self._deck["NORMAL"].append(card)

            plus_two: Card = Card(value=2, color=color)
            reverse: Card = Card(color=color, is_reverse=True)
            block: Card = Card(color=color, is_block=True)

        return None

    def _next_player(self, actual_player: Player) -> Player:
        index: int = self._players.index(actual_player)
        if self._reverse:
            return self._players[index - 1]
        elif index == self._num_players - 1:
            return self._players[0]

        return self._players[index + 1]

    def allowed_cards(self, card: Card) -> bool:
        if self._value_to_buy:
            return True
