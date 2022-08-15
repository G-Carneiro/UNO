from enum import Enum


class GameState(Enum):
    CREATED = 0
    WAITING = 1
    READY = 2
    RUNNING = 3
    CHOOSING = 4
    TERMINATED = 5
