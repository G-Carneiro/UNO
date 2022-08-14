from __future__ import annotations

from typing import List, Set, Optional

from .Card import Card
from .Color import Color


class Player:
    def __init__(self, name: str, id_: int) -> None:
        self._name: str = name
        self._id: int = id_
        self._cards: List[Card] = []

    def id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_cards(self) -> List[Card]:
        return self._cards

    def put_card(self, card: Card) -> None:
        self._cards.remove(card)
        return None

    def buy_card(self, card: Card) -> None:
        self._cards.append(card)
        return None

    def winner(self) -> bool:
        return (not len(self._cards))

    def have_allowed_card(self, allowed_cards: Set[Card]) -> bool:
        for card in self._cards:
            if card in allowed_cards:
                return True

        return False

    def put_allowed_card(self, allowed_cards: Set[Card]) -> Optional[Card]:
        for card in self._cards:
            if card in allowed_cards:
                self.put_card(card)
                return card

        return None

    def select_card(self, name: str) -> Optional[Card]:
        for card in self._cards:
            if (name.lower() == str(card).lower()):
                return card
        return None

    def num_cards(self) -> int:
        return len(self._cards)

    def num_color_card(self, color: Color) -> int:
        # TODO: change this method to attr
        num: int = 0
        for card in self._cards:
            if (card.get_color() == color):
                num += 1

        return num

    def __repr__(self) -> str:
        return self._name

    def __eq__(self, other: Player) -> bool:
        return (self._id == other.id())
