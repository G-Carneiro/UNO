from unittest import TestCase

from src.model.Card import Card
from src.model.CardType import CardType
from src.model.Color import Color
from src.model.Table import Table


class TableTests(TestCase):
    def setUp(self) -> None:
        self._table = Table()

    def test_deck(self) -> None:
        # Test number of cards.
        self.assertEqual(56, len(self._table._deck))

        # Test number of cards by color.
        black: Color = Color.BLACK
        usual_colors: list[Color] = [color for color in Color if color != black]

        for color in usual_colors:
            self.assertEqual(13, len(self._table._deck_by_key[color]))

        self.assertEqual(2, len(self._table._deck_by_key[black]))

        # Test number of reverse cards.
        self.assertEqual(4, len(self._table._deck_by_key[CardType.REVERSE]))

        # Test number of block cards.
        self.assertEqual(4, len(self._table._deck_by_key[CardType.SKIP]))

        # Test number of buy cards.
        self.assertEqual(5, len(self._table._deck_by_key[CardType.DRAW_TWO]))

        # Test number of change color cards.
        self.assertEqual(2, len(self._table._deck_by_key[CardType.CHANGE_COLOR]))

        # Test number of cards by value.
        for value in range(10):
            self.assertEqual(4, len(self._table._deck_by_key[CardType(value)]))

        # Test number of all cards in deck_by_key.
        cards: set[Card] = set()
        for value in self._table._deck_by_key.values():
            for card in value:
                cards.add(card)

        self.assertEqual(54, len(cards))

        return None

    def test_start_game(self) -> None:
        pass
