from __future__ import annotations

from typing import Optional

from .CardType import CardType
from .Color import Color


class Card:
    def __init__(self,
                 color: Color,
                 type_: CardType,
                 value: Optional[int] = None,
                 is_buy_card: bool = False,
                 is_reverse: bool = False,
                 is_block: bool = False,
                 is_change_color: bool = False) -> None:
        self._value: Optional[int] = value
        self._color: Color = color
        self._type: CardType = type_
        self._is_change_color: bool = is_change_color
        self._is_buy_card: bool = is_buy_card
        self._is_reverse: bool = is_reverse
        self._is_block: bool = is_block

    def get_color(self) -> Color:
        return self._color

    def get_value(self) -> Optional[int]:
        return self._value

    def get_type(self) -> CardType:
        return self._type

    def is_buy_card(self) -> bool:
        return self._is_buy_card

    def is_reverse(self) -> bool:
        return self._is_reverse

    def is_block(self) -> bool:
        return self._is_block

    def is_change_color(self) -> bool:
        return self._is_change_color

    def is_special(self) -> bool:
        return (self._is_buy_card or self._is_reverse or self._is_block or self._is_change_color)

    def __repr__(self) -> str:
        out: str = ""
        if self._is_buy_card:
            out += "+"

        if isinstance(self._value, int):
            out += str(self._value)
        else:
            out += str(self.get_type().name)

        if (self._color != Color.BLACK):
            out += str(self._color.name)

        return out

    def __str__(self) -> str:
        return self.__repr__()

    def __lt__(self, other: Card) -> bool:
        if (self._color.name != other.get_color().name):
            return (self._color.name < other.get_color().name)
        elif (self.get_type() != other.get_type()):
            return (self.get_type().value < other.get_type().value)

        return (other.get_value() is None)
