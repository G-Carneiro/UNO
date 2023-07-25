from __future__ import annotations

from enum import Enum


class CardType(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    DRAW_TWO = 10
    SKIP = 11
    REVERSE = 12
    CHANGE_COLOR = 13
    DRAW_FOUR = 14
    CALL_BLUFF = 15
    DRAW = 16

    def __lt__(self, other: CardType) -> bool:
        return (self.value < other.value)


INT: list[CardType] = [CardType(i) for i in range(10)]
