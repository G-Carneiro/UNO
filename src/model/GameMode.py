class GameMode:
    def __init__(self, mode: int | str = "10000111101111011011111",
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

    @property
    def black_over_black(self) -> bool:
        return bool(int(self.mode[-1]))

    @property
    def block_draw_four(self) -> bool:
        return bool(int(self.mode[-2]))

    @property
    def block_draw_two(self) -> bool:
        return bool(int(self.mode[-3]))

    @property
    def block_only_with_same_color(self) -> bool:
        return bool(int(self.mode[-4]))

    @property
    def block_reverse_draw(self) -> bool:
        return bool(int(self.mode[-5]))

    @property
    def call_bluff(self) -> bool:
        return bool(int(self.mode[-6]))

    @property
    def draw_four_over_draw_four(self) -> bool:
        return bool(int(self.mode[-7]))

    @property
    def draw_four_over_draw_two(self) -> bool:
        return bool(int(self.mode[-8]))

    @property
    def draw_two_only_with_same_color(self) -> bool:
        return bool(int(self.mode[-9]))

    @property
    def draw_two_over_draw_four(self) -> bool:
        return bool(int(self.mode[-10]))

    @property
    def draw_two_over_draw_two(self) -> bool:
        return bool(int(self.mode[-11]))

    @property
    def draw_while_no_card(self) -> bool:
        return bool(int(self.mode[-12]))

    @property
    def forced_play(self) -> bool:
        return bool(int(self.mode[-13]))

    @property
    def pass_after_draw(self) -> bool:
        return bool(int(self.mode[-14]))

    @property
    def pass_after_forced_draw(self) -> bool:
        return bool(int(self.mode[-15]))

    @property
    def reverse_draw_four(self) -> bool:
        return bool(int(self.mode[-16]))

    @property
    def reverse_draw_two(self) -> bool:
        return bool(int(self.mode[-17]))

    @property
    def reverse_only_with_same_color(self) -> bool:
        return bool(int(self.mode[-18]))

    @property
    def shuffle_hands(self) -> bool:
        return bool(int(self.mode[-19]))

    @property
    def swap_hand_after_play(self) -> bool:
        return bool(int(self.mode[-20]))

    @property
    def swap_hand(self) -> bool:
        return bool(int(self.mode[-21]))

    @property
    def swap_hands(self) -> bool:
        return bool(int(self.mode[-22]))

    @property
    def win_with_black(self) -> bool:
        return bool(int(self.mode[-23]))
