from __future__ import annotations

from enum import Enum


class Color(Enum):
    RED = "🟥"
    BLUE = "🟦"
    GREEN = "🟩"
    BLACK = "⬛"
    YELLOW = "🟨"

    def __str__(self) -> str:
        return f"{self.value} {self.name}"

    def __lt__(self, other: Color) -> bool:
        return (self.name < other.name)


BLACK: Color = Color.BLACK
COLORS: list[Color] = [color for color in Color if color != BLACK]
