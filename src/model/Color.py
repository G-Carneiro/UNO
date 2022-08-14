from enum import Enum
from typing import List


class Color(Enum):
    RED = "🟥"
    BLUE = "🟦"
    GREEN = "🟩"
    BLACK = "⬛"
    YELLOW = "🟨"

    def __str__(self) -> str:
        return f"{self.value} {self.name}"


BLACK: Color = Color.BLACK
COLORS: List[Color] = [color for color in Color if color != BLACK]
