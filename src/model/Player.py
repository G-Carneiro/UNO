from typing import List, Set, Optional

from .Card import Card


class Player:
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._cards: List[Card] = []

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

    def __repr__(self) -> str:
        return self._name
