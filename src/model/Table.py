from random import choice, shuffle
from typing import List, Dict, Set, Union, Optional

from .Card import Card
from .CardType import CardType
from .Color import Color
from .DoublyCircularList import DoublyCircularList
from .Node import DoublyLinkedListNode as Node
from .Player import Player

initial_cards_number: int = 7
max_cards_to_block: int = 10
block_buy_cards: bool = True
reverse_buy_cards: bool = True
buy_until_have_card: bool = True
play_before_buy: bool = False


class Table:
    def __init__(self) -> None:
        self._players_list: List[Player] = []
        self._players: DoublyCircularList = DoublyCircularList()
        self._actual_player_node: Optional[Node] = None
        self._value_to_buy: int = 0
        self._reverse: bool = False
        self._num_players: int = 0
        self._set_deck()

    def get_players(self) -> List[Player]:
        return self._players_list

    def get_player(self, player_id: int) -> Optional[Player]:
        for player in self._players_list:
            if (player.id() == player_id):
                return player
        return None

    def current_card(self) -> Card:
        return self._top_card

    def add_player(self, player: Player) -> None:
        self._players_list.append(player)
        return None

    def remove_player(self, player: Player) -> None:
        self._players_list.remove(player)
        return None

    def start_game(self) -> None:
        self._num_players = len(self._players_list)
        shuffle(self._players_list)

        if (not self._players.empty()):
            self._players.clear()

        for player in self._players_list:
            self._give_cards_to_player(player, num_cards=initial_cards_number)

        self._players.insert_values(self._players_list)
        self._actual_player_node = self._players.head()
        self._set_initial_top_card()

        return None

    def turn(self, selected: Union[Card, Color] = None) -> None:
        if isinstance(selected, Color):
            self._set_color(color=selected)
            self._next_player()
            return None

        current_player: Player = self.current_player()
        allowed_cards = self.allowed_cards()
        if (selected not in allowed_cards):
            if (not current_player.have_allowed_card(allowed_cards)):
                if (self._value_to_buy):
                    self._give_cards_to_player(current_player, self._value_to_buy)
                    self._value_to_buy = 0
                else:
                    while selected not in allowed_cards:
                        selected: Card = self.get_random_card()
                        current_player.buy_card(selected)
            return None

        self._play_card(card=selected)

        return None

    def current_player(self) -> Player:
        return self._actual_player_node.data()

    def _play_card(self, card: Card) -> None:
        self._set_color()
        self.current_player().put_card(card=card)
        self._top_card = card
        block: bool = False
        if self._top_card.is_reverse():
            self._reverse = not self._reverse
        elif self._top_card.is_buy_card():
            self._value_to_buy += self._top_card.get_value()
        elif self._top_card.is_block():
            if self._value_to_buy:
                self._value_to_buy = 0
            else:
                block = True

        if self._top_card.is_change_color():
            return None

        self._next_player(block=block)
        return None

    def _give_cards_to_player(self, player: Player, num_cards: int = 1) -> None:
        for _ in range(num_cards):
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
        self._color: Color = card.get_color()

        return None

    def _next_player(self, block: bool = False) -> Player:
        if (self._reverse):
            self._actual_player_node = self._actual_player_node.previous()
            if (block):
                self._actual_player_node = self._actual_player_node.previous()
        else:
            self._actual_player_node = self._actual_player_node.next()
            if (block):
                self._actual_player_node = self._actual_player_node.next()

        return (self._actual_player_node.data())

    def allowed_cards(self) -> Set[Card]:
        allowed_cards: Set[Card] = set()
        if (self._value_to_buy):
            allowed_cards |= set(self._deck_by_key[CardType.BUY])
            if (reverse_buy_cards):
                allowed_cards |= set(self._deck_by_key[CardType.REVERSE])
            if ((block_buy_cards) and (self._value_to_buy <= max_cards_to_block)):
                allowed_cards |= set(self._deck_by_key[CardType.BLOCK])
        else:
            # FIXME:
            if (self._top_card.get_type() == CardType.INT):
                allowed_cards |= set(self._deck_by_key[self._top_card.get_value()])
            else:
                allowed_cards |= set(self._deck_by_key[self._top_card.get_type()])
            allowed_cards |= set(self._deck_by_key[self._top_card.get_color()])
            allowed_cards |= set(self._deck_by_key[Color.BLACK])
            if (self._top_card.is_change_color()):
                allowed_cards |= set(self._deck_by_key[self._color])

        return allowed_cards

    def _set_color(self, color: Color = None) -> None:
        self._color = color
        return None

    def status(self) -> str:
        if (self._reverse):
            next_player: Node = self._actual_player_node.previous()
        else:
            next_player = self._actual_player_node.next()

        status: str = f"To draw: {self._value_to_buy} \n" \
                      f"Current card: {self._top_card} \n" \
                      f"Current player: {self.current_player()} ({self.current_player().num_cards()}) \n" \
                      f"Next players: {next_player.data()} ({len(next_player.data().get_cards())})"

        while True:
            if (self._reverse):
                next_player: Node = next_player.previous()
            else:
                next_player = next_player.next()

            if (next_player != self._actual_player_node):
                status += f" → {next_player.data()} ({len(next_player.data().get_cards())})"
            else:
                break

        return status

    def choosing_color(self) -> bool:
        return (self._top_card.is_change_color() and self._color is None)

    def __repr__(self) -> str:
        return str(self._players_list)
