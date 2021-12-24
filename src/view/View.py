from typing import List, Optional

from ..model.Player import Player
from ..model.Card import Card


class View:
    def __init__(self, player: Player) -> None:
        self._players: List[Player] = []
        self._player: Player = player
        self._top_card: Optional[Card] = None
        self._reverse: bool = False
        self._buy_cards: int = 0

    def set_reverse(self, reverse: bool = False) -> None:
        self._reverse = reverse
        return None

    def set_buy_cards(self, value: int) -> None:
        self._buy_cards = value
        return None

    def set_top_card(self, card: Card) -> None:
        self._top_card = card
        return None

    def draw_players(self) -> None:
        pass

    def draw_cards(self) -> None:
        pass

    def draw_table_infos(self) -> None:
        pass
