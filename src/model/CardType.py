from enum import Enum, auto


class CardType(Enum):
    BUY = auto()
    BLOCK = auto()
    REVERSE = auto()
    CHANGE_COLOR = auto()
