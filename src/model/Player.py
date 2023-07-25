from __future__ import annotations

from typing import Optional

from .Card import CALL_BLUFF, Card, DRAW
from .Color import BLACK, Color


class Player:
    def __init__(self, name: str, id_: int) -> None:
        self._name: str = name
        self._id: int = id_
        self._cards: list[Card] = []
        self._num_color_cards: dict[Color, int] = {color: 0 for color in Color}
        self._bluffing: bool = False

    @property
    def bluffing(self) -> bool:
        return self._bluffing

    @bluffing.setter
    def bluffing(self, value: bool):
        self._bluffing = value

    def id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_cards(self) -> list[Card]:
        return self._cards

    def drop_hand(self) -> None:
        while (not self.winner()):
            self.put_card(self._cards[0])

        return None

    def put_card(self, card: Card) -> None:
        self._cards.remove(card)
        self._num_color_cards[card.color] -= 1
        return None

    def draw_card(self, card: Card) -> None:
        index: int = self.num_cards()
        for i in range(self.num_cards()):
            if (card < self._cards[i]):
                index = i
                break
        self._cards.insert(index, card)
        self._num_color_cards[card.color] += 1
        return None

    def winner(self) -> bool:
        return (not 0 < self.num_cards() < 100)

    def uno(self) -> bool:
        return (self.num_cards() == 1)

    def have_playable_card(self, playable_cards: set[Card]) -> bool:
        for card in self._cards:
            if card in playable_cards:
                return True

        return False

    def not_have_playable_card(self, playable_cards: set[Card]) -> bool:
        return (not self.have_playable_card(playable_cards=playable_cards))

    def put_playable_card(self, playable_cards: set[Card]) -> Optional[Card]:
        for card in self._cards:
            if card in playable_cards:
                self.put_card(card)
                return card

        return None

    def select_card(self, name: str) -> Optional[Card]:
        for card in self._cards + [CALL_BLUFF, DRAW]:
            if (name.lower() == str(card).lower()):
                return card
        return None

    def num_cards(self) -> int:
        return len(self._cards)

    def num_color_card(self, color: Color) -> int:
        return self._num_color_cards[color]

    def main_color(self) -> Color:
        black_cards: int = self.num_color_card(color=BLACK)
        self._num_color_cards[BLACK] = 0
        main: Color = max(self._num_color_cards, key=self._num_color_cards.get)
        self._num_color_cards[BLACK] = black_cards

        return main

    def __repr__(self) -> str:
        return self._name

    def __eq__(self, other: Player) -> bool:
        return (self._id == other.id())
