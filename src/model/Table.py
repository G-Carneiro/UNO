from random import choice, randint
from typing import Optional

from .Card import Card
from .CardType import CardType
from .Color import BLACK, Color, COLORS
from .DoublyCircularList import DoublyCircularList
from .exceptions import *
from .GameState import GameState
from .Node import DoublyLinkedListNode as Node
from .Player import Player
from ..utils.settings import *


class Table:
    def __init__(self) -> None:
        self._players: DoublyCircularList = DoublyCircularList()
        self._value_to_buy: int = 0
        self._reverse: bool = False
        self._state: GameState = GameState.CREATED
        self._playable_cards: set[Card] = set()
        self._set_deck()

    def get_players(self):
        return self._players

    @property
    def state(self) -> GameState:
        return self._state

    def num_players(self) -> int:
        return self._players.size

    def get_player(self, player_id: int) -> Optional[Player]:
        for player in self.get_players():
            if (player.id() == player_id):
                return player
        return None

    def current_card(self) -> Card:
        return self._top_card

    def add_player(self, player: Player) -> None:
        if (player in self._players):
            raise AlreadyJoined

        # new player can't join as current player
        index: int = randint(self.running(), self.num_players())
        self._players.insert(data=player, index=index)
        self._give_cards_to_player(player, num_cards=INITIAL_CARDS_NUMBER)

        if (self.num_players() >= MIN_PLAYERS):
            self._state = GameState.READY

        return None

    def remove_player(self, player: Player) -> None:
        if (self.running()):
            if (player == self.current_player()):
                self.next_player()

        if (self._players.contains(player)):
            self._players.remove(data=player)
        else:
            raise NotInGame

        if (self.num_players() < MIN_PLAYERS):
            self._state = GameState.WAITING

        return None

    def start_game(self) -> None:
        if (not self.ready()):
            raise GameNotReady

        steps: int = randint(0, self.num_players())
        self._players.head_to_next(steps=steps)

        self._set_initial_card()
        self._compute_playable_cards()

        return None

    def turn(self, selected: Card | Color = None) -> None:
        if isinstance(selected, Color):
            self._set_color(color=selected)
            self.next_player()
            return None

        current_player: Player = self.current_player()
        playable_cards = self.playable_cards
        if (selected not in playable_cards):
            if (current_player.not_have_playable_card(playable_cards=playable_cards)):
                if (self._value_to_buy):
                    self._give_cards_to_player(current_player, self._value_to_buy)
                    self._value_to_buy = 0
                    if PASS_AFTER_FORCED_DRAW:
                        self.next_player()
                else:
                    card: Card = self.get_random_card()
                    current_player.draw_card(card)
                    if DRAW_WHILE_NO_CARD:
                        while card not in playable_cards:
                            card: Card = self.get_random_card()
                            current_player.draw_card(card)

                    if PASS_AFTER_DRAW:
                        self.next_player()
            else:
                return None
        else:
            self._play_card(card=selected)

        return None

    def current_player(self) -> Player:
        return self._players.head.data()

    def _current_node(self) -> Node:
        return self._players.head

    def _play_card(self, card: Card) -> None:
        self.current_player().put_card(card=card)
        if (SWAP_HAND_AFTER_PLAY):
            self._swap_hand_after_play()

        self._top_card = card
        self._set_color()
        block: bool = False
        if self._top_card.is_reverse():
            if (self.num_players() != 2):
                self._reverse = not self._reverse
            elif (not self._value_to_buy):
                block = True
        elif self._top_card.is_buy_card():
            self._value_to_buy += self._top_card.value
        elif self._top_card.is_skip():
            if self._value_to_buy:
                self._value_to_buy = 0
            else:
                block = True

        if self._top_card.is_change_color():
            self._state = GameState.CHOOSING
            return None

        self.next_player(block=block)
        return None

    def _give_cards_to_player(self, player: Player, num_cards: int = 1) -> None:
        for _ in range(num_cards):
            player.draw_card(self.get_random_card())
        return None

    def _swap_hand_after_play(self) -> None:
        num_cards: int = self.current_player().num_cards()
        self.current_player().drop_hand()
        self._give_cards_to_player(player=self.current_player(), num_cards=num_cards)
        return None

    def _set_deck(self) -> None:
        self._deck: list[Card] = []
        self._deck_by_key: dict[Color | CardType, list[Card]] = {}

        for color in Color:
            self._deck_by_key[color] = []

        for card_type in CardType:
            self._deck_by_key[card_type] = []

        for color in COLORS:
            for value in range(10):
                card_type: CardType = CardType(value=value)
                card = Card(value=value, color=color, type_=card_type)
                self._deck_by_key[color].append(card)
                self._deck_by_key[card_type].append(card)
                self._deck.append(card)

            draw_two: Card = Card(value=2, color=color, type_=CardType.DRAW_TWO)
            self._deck_by_key[CardType.DRAW_TWO].append(draw_two)

            skip: Card = Card(color=color, type_=CardType.SKIP)
            self._deck_by_key[CardType.SKIP].append(skip)

            reverse: Card = Card(color=color, type_=CardType.REVERSE)
            self._deck_by_key[CardType.REVERSE].append(reverse)

            self._deck_by_key[color] += [draw_two, skip, reverse]
            self._deck += [draw_two, skip, reverse]

        draw_four: Card = Card(value=4, color=BLACK, type_=CardType.DRAW_FOUR)
        self._deck_by_key[CardType.DRAW_FOUR].append(draw_four)

        change_color: Card = Card(color=BLACK, type_=CardType.CHANGE_COLOR)

        self._deck_by_key[BLACK] += [draw_four, change_color]
        self._deck_by_key[CardType.CHANGE_COLOR] += [draw_four, change_color]
        self._deck += [draw_four, draw_four, change_color, change_color]

        return None

    def get_random_card(self) -> Card:
        return choice(self._deck)

    def _set_initial_card(self) -> None:
        card: Card = self.get_random_card()

        while card.is_special():
            card = self.get_random_card()

        self._top_card: Card = card
        self._set_color()

        return None

    def next_player(self, block: bool = False) -> None:
        if (self.current_player().winner()):
            self._state = GameState.TERMINATED
            return None

        steps: int = 1 + block

        if (self._reverse):
            self._players.head_to_previous(steps=steps)
        else:
            self._players.head_to_next(steps=steps)

        self._compute_playable_cards()
        return None

    @property
    def playable_cards(self) -> set[Card]:
        return self._playable_cards

    def _compute_playable_cards(self) -> None:
        playable_cards: set[Card] = set()
        if (self._value_to_buy):
            if (self._top_card.is_draw_two()):
                self._compute_draw_case(playable_cards=playable_cards,
                                        draw_four_over_draw=DRAW_FOUR_OVER_DRAW_TWO,
                                        draw_two_over_draw=DRAW_TWO_OVER_DRAW_TWO,
                                        block_draw=BLOCK_DRAW_TWO,
                                        reverse_draw=REVERSE_DRAW_TWO)
            elif (self._top_card.is_draw_four()):
                self._compute_draw_case(playable_cards=playable_cards,
                                        draw_four_over_draw=DRAW_FOUR_OVER_DRAW_FOUR,
                                        draw_two_over_draw=DRAW_TWO_OVER_DRAW_FOUR,
                                        block_draw=BLOCK_DRAW_FOUR,
                                        reverse_draw=REVERSE_DRAW_FOUR)
            else:  # card is reverse, then REVERSE_DRAW enabled
                playable_cards |= set(self._deck_by_key[CardType.DRAW_TWO])
                playable_cards |= set(self._deck_by_key[CardType.DRAW_FOUR])
                reverses: set[Card] = set(self._deck_by_key[CardType.REVERSE])
                if (REVERSE_ONLY_WITH_SAME_COLOR):
                    reverses &= set(self._deck_by_key[self._color])

                playable_cards |= reverses
                if ((BLOCK_REVERSE_DRAW) and (self._value_to_buy <= MAX_TO_BLOCK)):
                    blocks: set[Card] = set(self._deck_by_key[CardType.SKIP])
                    if (BLOCK_ONLY_WITH_SAME_COLOR):
                        blocks &= set(self._deck_by_key[self._color])
                    playable_cards |= blocks
        else:
            playable_cards |= set(self._deck_by_key[self._top_card.type])
            playable_cards |= set(self._deck_by_key[self._color])
            if (BLACK_OVER_BLACK or not self._top_card.is_black()):
                playable_cards |= set(self._deck_by_key[BLACK])

        if (self.current_player().uno() and not WIN_WITH_BLACK):
            playable_cards -= set(self._deck_by_key[BLACK])

        self._playable_cards = playable_cards
        return None

    def _compute_draw_case(self,
                           playable_cards: set[Card],
                           draw_four_over_draw: bool,
                           draw_two_over_draw: bool,
                           block_draw: bool,
                           reverse_draw: bool
                           ) -> None:
        if (draw_four_over_draw):
            playable_cards |= set(self._deck_by_key[CardType.DRAW_FOUR])
        if (draw_two_over_draw):
            draw_two_cards: set[Card] = set(self._deck_by_key[CardType.DRAW_TWO])
            if (DRAW_TWO_ONLY_WITH_SAME_COLOR):
                draw_two_cards &= set(self._deck_by_key[self._color])
            playable_cards |= draw_two_cards
        if ((reverse_draw) and (self._value_to_buy <= MAX_TO_REVERSE)):
            reverses: set[Card] = set(self._deck_by_key[CardType.REVERSE])
            if (REVERSE_ONLY_WITH_SAME_COLOR):
                reverses &= set(self._deck_by_key[self._color])
            playable_cards |= reverses
        if ((block_draw) and (self._value_to_buy <= MAX_TO_BLOCK)):
            blocks: set[Card] = set(self._deck_by_key[CardType.SKIP])
            if (BLOCK_ONLY_WITH_SAME_COLOR):
                blocks &= set(self._deck_by_key[self._color])
            playable_cards |= blocks
        return None

    def _set_color(self, color: Color = None) -> None:
        if (color is None):
            self._color = self._top_card.color
        else:
            self._color = color
        self._state = GameState.RUNNING
        return None

    def status(self) -> str:
        if (self._reverse):
            next_player: Node = self._current_node().previous()
        else:
            next_player = self._current_node().next()

        status: str = f"To draw: {self._value_to_buy} \n" \
                      f"Current card: {self._top_card}{self._top_card.color.value} \n" \
                      f"Current player: {self.current_player()} (" \
                      f"{self.current_player().num_cards()}) \n" \
                      f"Next players: {next_player.data()} ({next_player.data().num_cards()})"

        while True:
            if (self._reverse):
                next_player: Node = next_player.previous()
            else:
                next_player = next_player.next()

            if (next_player != self._current_node()):
                status += f" → {next_player.data()} ({next_player.data().num_cards()})"
            else:
                break

        return status

    def choosing_color(self) -> bool:
        return (self._state == GameState.CHOOSING)

    def terminated(self) -> bool:
        return (self._state == GameState.TERMINATED)

    def running(self) -> bool:
        return (self._state == GameState.RUNNING)

    def ready(self) -> bool:
        return (self._state == GameState.READY)

    def __repr__(self) -> str:
        return f"{str(self._players)} - {str(self.current_card())}"
