from typing import List, Dict, Set, Union

from .Card import Card
from .Color import Color
from .Player import Player
from .CardType import CardType


class Table:
    def __init__(self) -> None:
        self._players: List[Player] = []
        self._value_to_buy: int = 0
        self._allowed_cards: Set[Card] = set()
        self._set_deck()
        self._top_card: Card = None         # FIXME: type
        self._reverse: bool = False
        self._num_players: int = len(self._players)

    def get_players(self) -> List[Player]:
        return self._players

    def add_player(self, player: Player) -> None:
        self._players.append(player)
        return None

    def remove_player(self, player: Player) -> None:
        self._players.remove(player)
        return None

    def _set_deck(self) -> None:
        self._deck: List[Card] = []
        self._deck_by_key: Dict[Union[Color, CardType, int], List[Card]] = {}

        for value in range(10):
            self._deck_by_key[value] = []

        for color in Color:
            self._deck_by_key[color] = []

        for card_type in CardType:
            self._deck_by_key[card_type] = []

        black: Color = Color.BLACK
        usual_colors: List[Color] = [color for color in Color if color != black]

        for color in usual_colors:
            for value in range(10):
                card = Card(value=value, color=color)
                self._deck_by_key[color].append(card)
                self._deck_by_key[value].append(card)
                self._deck.append(card)

            plus_two: Card = Card(value=2, color=color, is_buy_card=True)
            self._deck_by_key[CardType.BUY].append(plus_two)

            block: Card = Card(color=color, is_block=True)
            self._deck_by_key[CardType.BLOCK].append(block)

            reverse: Card = Card(color=color, is_reverse=True)
            self._deck_by_key[CardType.REVERSE].append(reverse)

            self._deck_by_key[color] += [plus_two, block, reverse]
            self._deck += [plus_two, block, reverse]

        plus_four: Card = Card(value=4, color=black, is_buy_card=True, is_change_color=True)
        self._deck_by_key[CardType.BUY].append(plus_four)

        change_color: Card = Card(color=black, is_change_color=True)

        self._deck_by_key[black] += [plus_four, change_color]
        self._deck_by_key[CardType.CHANGE_COLOR] += [plus_four, change_color]
        self._deck += [plus_four, plus_four, change_color, change_color]

        return None

    def _next_player(self, actual_player: Player) -> Player:
        index: int = self._players.index(actual_player)
        if self._reverse:
            return self._players[index - 1]
        elif index == self._num_players - 1:
            return self._players[0]

        return self._players[index + 1]

    def allowed_cards(self, card: Card) -> bool:
        if self._value_to_buy:
            return True
