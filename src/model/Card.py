from typing import Optional, Union

from .Color import Color
from .CardType import CardType


class Card:
    def __init__(self,
                 color: Color,
                 value: Optional[int] = None,
                 is_buy_card: bool = False,
                 is_reverse: bool = False,
                 is_block: bool = False,
                 is_change_color: bool = False) -> None:
        self._value: Optional[int] = value
        self._color: Color = color
        self._is_change_color: bool = is_change_color
        self._is_buy_card: bool = is_buy_card
        self._is_reverse: bool = is_reverse
        self._is_block: bool = is_block

    def get_color(self) -> Color:
        return self._color

    def get_value(self) -> Optional[int]:
        return self._value

    def get_type(self) -> Union[CardType, int]:
        if self._is_reverse:
            return CardType.REVERSE
        elif self._is_block:
            return CardType.BLOCK
        elif self._is_change_color:
            return CardType.CHANGE_COLOR
        else:
            return self._value

    def is_buy_card(self) -> bool:
        return self._is_buy_card

    def is_special(self) -> bool:
        return (self._is_buy_card or self._is_reverse or self._is_block or self._is_change_color)
