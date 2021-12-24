from enum import Enum, auto
from typing import Tuple

from ..view.colors import *


class Color(Enum):
    RED = auto()
    BLUE = auto()
    GREEN = auto()
    BLACK = auto()
    YELLOW = auto()

    def get_rgb_color(self) -> Tuple[int, int, int]:
        name: str = self.name.lower()
        if (name == "blue"):
            color_: color = blue
        elif (name == "red"):
            color_: color = red
        elif (name == "green"):
            color_: color = green
        elif (name == "yellow"):
            color_: color = yellow
        else:
            color_: color = black

        return color_
