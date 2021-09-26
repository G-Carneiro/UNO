from typing import Optional

from .Color import Color


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
