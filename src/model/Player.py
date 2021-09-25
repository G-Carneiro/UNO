from typing import List

from .Card import Card


class Player:
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._cards: List[Card] = []

    def put_card(self, card: Card) -> None:
        self._cards.remove(card)
        return None

    def buy_card(self, card: Card) -> None:
        self._cards.append(card)
        return None
