with open("../utils/settings.py", "r") as sett:
    with open("../model/GameMode.py", "w") as mode:
        lines = sett.readlines()
        index = 0
        mode.write("""class GameMode:
    def __init__(self, mode: int | str = "1000000111011110110001011100",
                 num_cards: int = 7,
                 max_to_block: int = 10,
                 max_to_reverse: int = 20,
                 min_players: int = 2,
                 timeout: int = 60
                 ) -> None:
        self.num_cards: int = num_cards
        self.max_to_block: int = max_to_block
        self.max_to_reverse: int = max_to_reverse
        self.min_players: int = min_players
        self.timeout: int = timeout
        self._set_all_settings(mode=mode)

    def set_mode(self, mode: int | str) -> None:
        return self._set_all_settings(mode=mode)
    
    def _bit_to_bool(self, index: int) -> bool:
        return bool(int(self._mode[index]))

    def _set_all_settings(self, mode: int | str) -> None:
        if isinstance(mode, str):
            mode = int(mode, 2)

        self._mode: str = f"{mode:{0}{TOTAL_BITS}b}"
        if len(self._mode) > TOTAL_BITS:
            raise ValueError\n""")
        for line in lines:
            split = line.replace(": bool ", "").split("=")
            if (split[0][0] != "#"):
                index -= 1
                mode.write(f"        self.{split[0].lower()}: bool = "
                           f"self._bit_to_bool(index={index})\n")
    with open("../model/GameMode.py", "r") as mode:
        mode_lines = mode.readlines()
    with open("../model/GameMode.py", "w") as mode:
        mode_lines = [f"TOTAL_BITS: int = {-index}\n", "\n", "\n"] + mode_lines
        mode.writelines(mode_lines)
