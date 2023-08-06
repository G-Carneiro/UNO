from enum import auto, Enum


class Action(Enum):
    CALL_BLUFF = auto()
    DRAW = auto()
    PASS = auto()
