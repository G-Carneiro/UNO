from typing import List, Dict, Set, Union
from random import choice, shuffle

from .Card import Card
from .Color import Color
from .Player import Player
from .CardType import CardType


initial_cards_number: int = 7


class Table:
    def __init__(self) -> None:
        self._players: List[Player] = []
        self._value_to_buy: int = 0
        self._reverse: bool = False
        self._num_players: int = 0
        self._set_deck()

    def get_players(self) -> List[Player]:
        return self._players

    def add_player(self, player: Player) -> None:
        self._players.append(player)
        return None

    def remove_player(self, player: Player) -> None:
        self._players.remove(player)
        return None

    def start_game(self) -> None:
        self._num_players = len(self._players)
        shuffle(self._players)
        for player in self._players:
            for _ in range(initial_cards_number + 1):
                self._give_card_to_player(player)
        self._set_initial_top_card()
        # self._run()

        return None

    def _run(self) -> None:
        actual_player: Player = self._players[-1]

        while not actual_player.winner():
            actual_player = self._next_player(actual_player)
            if actual_player.have_allowed_card(self.allowed_cards()):
                pass
            else:
                card: Card = self.get_random_card()
                actual_player.buy_card(card)
                while card not in self.allowed_cards():
                    card: Card = self.get_random_card()
                    actual_player.buy_card(card)

    def _give_card_to_player(self, player: Player) -> None:
        player.buy_card(self.get_random_card())
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

    def get_random_card(self) -> Card:
        return choice(self._deck)

    def _set_initial_top_card(self) -> None:
        card: Card = self.get_random_card()

        while card.is_special():
            card = self.get_random_card()

        self._top_card: Card = card

        return None

    def _next_player(self, actual_player: Player, block: bool = False) -> Player:
        index: int = self._players.index(actual_player)
        operand: int = 1 + block
        if self._reverse:
            return self._players[index - operand]
        elif index == self._num_players - operand:
            return self._players[0]

        return self._players[index + 1]

    def allowed_cards(self) -> Set[Card]:
        allowed_cards: Set[Card] = set()
        if self._value_to_buy:
            allowed_cards |= self._deck_by_key[CardType.BUY]
            allowed_cards |= self._deck_by_key[CardType.REVERSE]
            if self._value_to_buy <= 10:
                allowed_cards |= self._deck_by_key[CardType.BLOCK]
        else:
            allowed_cards |= self._deck_by_key[self._top_card.get_type()]
            allowed_cards |= self._deck_by_key[self._top_card.get_color()]
            allowed_cards |= self._deck_by_key[Color.BLACK]

        return allowed_cards

