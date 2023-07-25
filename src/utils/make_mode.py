with open("../utils/settings.py", "r") as sett:
    with open("../model/GameMode.py", "w") as mode:
        lines = sett.readlines()
        index = -1
        mode.write("""class GameMode:
    def __init__(self, mode: int | str = "1000001110111101111011100",
                 num_cards: int = 7,
                 max_to_block: int = 10,
                 max_to_reverse: int = 20,
                 min_players: int = 2,
                 timeout: int = 60
                 ) -> None:
        if isinstance(mode, int):
            mode = bin(mode)[2:]

        self.mode: str = mode
        self.num_cards: int = num_cards
        self.max_to_block: int = max_to_block
        self.max_to_reverse: int = max_to_reverse
        self.min_players: int = min_players
        self.timeout: int = timeout\n""")
        for line in lines:
            split = line.replace(": bool ", "").split("=")
            if (split[0][0] != "#"):
                mode.write(f"        self.{split[0].lower()}: bool = "
                           f"self._bit_to_bool(index={index})\n")
                index -= 1
        mode.write(f"\n"
                   f"    def _bit_to_bool(self, index: int) -> bool:\n"
                   f"        return bool(int(self.mode[index]))\n")
