from unittest import TestCase

from src.model.Card import Card
from src.model.Color import Color
from src.model.Player import Player
from src.view.View import View


class ViewTests(TestCase):
    def setUp(self) -> None:
        self._view: View = View()
        return None

    def test_menu_screen(self) -> None:
        self._view._players = [Player("Gabriel"), Player("Thyago")]
        player = self._view._player = Player("Gabriel")
        for _ in range(20):
            card: Card = Card(color=Color.RED, value=2)
            player._cards.append(card)

        self._view.update_window()




