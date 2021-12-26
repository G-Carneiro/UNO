from unittest import TestCase

from src.model.Player import Player
from src.model.Table import Table
from src.view.View import View


class ViewTests(TestCase):
    def setUp(self) -> None:
        self._view: View = View()
        return None

    def test_menu_screen(self) -> None:
        table = Table()
        player = self._view._player = Player("Gabriel")
        self._view._players = [player, Player("Thyago")]
        for _ in range(10):
            self._view.add_card(table.get_random_card())

        self._view.update_window()




