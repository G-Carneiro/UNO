from __future__ import annotations

from typing import Optional

from .CardType import CardType, INT
from .Color import Color, BLACK


class Card:
    def __init__(self,
                 color: Color,
                 type_: CardType,
                 value: Optional[int] = None,
                 ) -> None:
        self._value: Optional[int] = value
        self._color: Color = color
        self._type: CardType = type_

    def get_color(self) -> Color:
        return self._color

    def get_value(self) -> Optional[int]:
        return self._value

    def get_type(self) -> CardType:
        return self._type

    def is_buy_card(self) -> bool:
        return (self._type == CardType.BUY or self._type == CardType.PLUS_FOUR)

    def is_reverse(self) -> bool:
        return (self._type == CardType.REVERSE)

    def is_block(self) -> bool:
        return (self._type == CardType.BLOCK)

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
            out += str(self.get_type().name)

        if (self._color != BLACK):
            out += str(self._color.name)

        return out

    def __str__(self) -> str:
        return self.__repr__()

    def __lt__(self, other: Card) -> bool:
        if (self._color != other.get_color()):
            return (self._color < other.get_color())

        return (self.get_type() < other.get_type())
