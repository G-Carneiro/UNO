from __future__ import annotations

from typing import List, Set, Optional, Dict

from .Card import Card
from .Color import Color
from ..utils.settings import WIN_WITH_BLACK


class Player:
    def __init__(self, name: str, id_: int) -> None:
        self._name: str = name
        self._id: int = id_
        self._cards: List[Card] = []
        self._num_color_cards: Dict[Color, int] = {color: 0 for color in Color}

    def id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_cards(self) -> List[Card]:
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
        # FIXME: solve the problem when player have more than 50 cards in telegram bot
        return (not 0 < self.num_cards() <= 50)

    def uno(self) -> bool:
        return (self.num_cards() == 1)

    def have_playable_card(self, playable_cards: Set[Card]) -> bool:
        if (not WIN_WITH_BLACK and self.uno() and self._cards[0].is_black()):
            return False
        for card in self._cards:
            if card in playable_cards:
                return True

        return False

    def not_have_playable_card(self, playable_cards: Set[Card]) -> bool:
        return (not self.have_playable_card(playable_cards=playable_cards))

    def put_playable_card(self, playable_cards: Set[Card]) -> Optional[Card]:
        for card in self._cards:
            if card in playable_cards:
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
        return self._num_color_cards[color]

    def __repr__(self) -> str:
        return self._name

    def __eq__(self, other: Player) -> bool:
        return (self._id == other.id())
