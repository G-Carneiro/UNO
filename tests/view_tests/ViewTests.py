from unittest import TestCase

from src.model.Card import Card
from src.model.Color import Color
from src.model.Player import Player
from src.view.View import View
from src.model.Table import Table


class ViewTests(TestCase):
    def setUp(self) -> None:
        self._view: View = View()
        return None

    def test_menu_screen(self) -> None:
        table = Table()
        self._view._players = [Player("Gabriel"), Player("Thyago")]
        player = self._view._player = Player("Gabriel")
        # card: Card = Card(color=Color.RED, value=2)
        for _ in range(20):
            self._view.add_card(table.get_random_card())

        self._view.update_window()




