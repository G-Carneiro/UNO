from __future__ import annotations

from typing import Optional

from .CardType import CardType, INT
from .Color import BLACK, Color


class Card:
    def __init__(self,
                 color: Color,
                 type_: CardType,
                 value: Optional[int] = None,
                 ) -> None:
        self._value: Optional[int] = value
        self._color: Color = color
        self._type: CardType = type_

    @property
    def color(self) -> Color:
        return self._color

    @property
    def value(self) -> Optional[int]:
        return self._value

    @property
    def type(self) -> CardType:
        return self._type

    def is_draw_two(self) -> bool:
        return (self._type == CardType.DRAW_TWO)

    def is_draw_four(self) -> bool:
        return (self._type == CardType.DRAW_FOUR)

    def is_buy_card(self) -> bool:
        return (self._type == CardType.DRAW_TWO or self._type == CardType.DRAW_FOUR)

    def is_reverse(self) -> bool:
        return (self._type == CardType.REVERSE)

    def is_skip(self) -> bool:
        return (self._type == CardType.SKIP)

    def is_change_color(self) -> bool:
        return (self._color == BLACK)

    def is_special(self) -> bool:
        return (self._type not in INT)

    def is_black(self) -> bool:
        return (self._color == BLACK)

    def __repr__(self) -> str:
        out: str = ""
        if self.is_buy_card():
            out += "+"

        if isinstance(self._value, int):
            out += str(self._value)
        else:
            out += str(self.type.name)

        if (self._color != BLACK):
            out += str(self._color.name)

        return out

    def __str__(self) -> str:
        return self.__repr__()

    def __lt__(self, other: Card) -> bool:
        if (self._color != other.color):
            return (self._color < other.color)

        return (self.type < other.type)


CALL_BLUFF: Card = Card(color=BLACK, type_=CardType.CALL_BLUFF)
DRAW: Card = Card(color=BLACK, type_=CardType.DRAW)
