from .Color import Color


class Card:
    def __init__(self, value: int, color: Color, is_buy_card: bool = False) -> None:
        self._value: int = value
        self._color: Color = color
        self._is_buy_card: bool = is_buy_card

    def get_color(self) -> Color:
        return self._color

    def get_value(self) -> int:
        return self._value
