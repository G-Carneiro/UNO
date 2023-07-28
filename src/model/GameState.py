from enum import auto, Enum


class GameState(Enum):
    CREATED = auto()
    WAITING = auto()
    READY = auto()
    RUNNING = auto()
    CHOOSING_CARD = auto()
    CHOOSING_COLOR = auto()
    CHOOSING_EFFECT = auto()
    CHOOSING_PLAYER = auto()
    TERMINATED = auto()
