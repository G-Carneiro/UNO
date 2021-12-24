from typing import List, Optional

from pygame import display, font

from ..model.Card import Card
from ..model.Player import Player


class View:
    def __init__(self,
                 player: Player,
                 width: int = 700,
                 height: int = 700,
                 caption: str = "UNO - Client"
                 ) -> None:
        self._players: List[Player] = []
        self._player: Player = player
        self._width: int = width
        self._height: int = height
        self._top_card: Optional[Card] = None
        self._reverse: bool = False
        self._buy_cards: int = 0
        self._window: display = display.set_mode((width, height))
        self._window_configuration(caption)

    @staticmethod
    def _window_configuration(caption: str) -> None:
        display.set_caption(caption)
        font.init()
        return None

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

    def update_window(self) -> None:
        pass
