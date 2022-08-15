from __future__ import annotations

from enum import Enum
from typing import List


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
    BUY = 10
    BLOCK = 11
    REVERSE = 12
    CHANGE_COLOR = 13
    PLUS_FOUR = 14

    def __lt__(self, other: CardType) -> bool:
        return (self.value < other.value)


INT: List[CardType] = [CardType(i) for i in range(10)]
