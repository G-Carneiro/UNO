class GameMode:
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
        self.timeout: int = timeout
        self.auto_choose_color: bool = self._bit_to_bool(index=-1)
        self.auto_skip: bool = self._bit_to_bool(index=-2)
        self.black_over_black: bool = self._bit_to_bool(index=-3)
        self.block_draw_four: bool = self._bit_to_bool(index=-4)
        self.block_draw_two: bool = self._bit_to_bool(index=-5)
        self.block_only_with_same_color: bool = self._bit_to_bool(index=-6)
        self.block_reverse_draw: bool = self._bit_to_bool(index=-7)
        self.call_bluff: bool = self._bit_to_bool(index=-8)
        self.draw_four_over_draw_four: bool = self._bit_to_bool(index=-9)
        self.draw_four_over_draw_two: bool = self._bit_to_bool(index=-10)
        self.draw_two_only_with_same_color: bool = self._bit_to_bool(index=-11)
        self.draw_two_over_draw_four: bool = self._bit_to_bool(index=-12)
        self.draw_two_over_draw_two: bool = self._bit_to_bool(index=-13)
        self.draw_while_no_card: bool = self._bit_to_bool(index=-14)
        self.forced_play: bool = self._bit_to_bool(index=-15)
        self.pass_after_draw: bool = self._bit_to_bool(index=-16)
        self.pass_after_forced_draw: bool = self._bit_to_bool(index=-17)
        self.reverse_draw_four: bool = self._bit_to_bool(index=-18)
        self.reverse_draw_two: bool = self._bit_to_bool(index=-19)
        self.reverse_only_with_same_color: bool = self._bit_to_bool(index=-20)
        self.shuffle_hands: bool = self._bit_to_bool(index=-21)
        self.shuffle_hands_equally: bool = self._bit_to_bool(index=-22)
        self.swap_hand_after_play: bool = self._bit_to_bool(index=-23)
        self.swap_hand: bool = self._bit_to_bool(index=-24)
        self.swap_hands: bool = self._bit_to_bool(index=-25)
        self.win_with_black: bool = self._bit_to_bool(index=-26)

    def _bit_to_bool(self, index: int) -> bool:
        return bool(int(self.mode[index]))
