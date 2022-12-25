class GameMode:
    def __init__(self, mode: int | str = "1111101111110111100001",
                 num_cards: int = 7,
                 max_to_block: int = 10,
                 max_to_reverse: int = 20,
                 min_players: int = 2,
                 ) -> None:
        if isinstance(mode, int):
            mode = bin(mode)[2:]

        self._mode: str = mode
        self._num_cards: int = num_cards
        self._max_to_block: int = max_to_block
        self._max_to_reverse: int = max_to_reverse
        self._min_players: int = min_players

    @property
    def num_cards(self) -> int:
        return self._num_cards

    @property
    def max_to_block(self) -> int:
        return self._max_to_block

    @property
    def black_over_black(self) -> bool:
        return bool(int(self._mode[0]))

    @property
    def block_draw_four(self) -> bool:
        return bool(int(self._mode[1]))
