from typing import List, Optional

from pygame import display, font, event, QUIT, quit
from pygame.time import Clock
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox

from ..model.Card import Card
from ..model.Player import Player
from .colors import *

button_width: int = 100
button_height: int = 50


class View:
    def __init__(self,
                 width: int = 700,
                 height: int = 700,
                 caption: str = "UNO - Client"
                 ) -> None:
        self._players: List[Player] = []
        self._player: Optional[Player] = None
        self._width: int = width
        self._height: int = height
        self._top_card: Optional[Card] = None
        self._reverse: bool = False
        self._buy_cards: int = 0
        self._buttons: List[Button] = []
        self._window: display = display.set_mode((width, height))
        self._window_configuration(caption)
        self._menu_screen()

    @staticmethod
    def _window_configuration(caption: str) -> None:
        display.set_caption(caption)
        font.init()
        return None

    def set_reverse(self, reverse: bool = False) -> None:
        self._reverse = reverse
        return None

    def set_buy_cards(self, value: int) -> None:
        self._buy_cards = value
        return None

    def set_top_card(self, card: Card) -> None:
        self._top_card = card
        return None

    def _add_button(self, card: Card) -> None:
        name: str = card.get_color().name.lower()
        if (name == "blue"):
            button_color: color = blue
        elif (name == "red"):
            button_color: color = red
        elif (name == "green"):
            button_color: color = green
        elif (name == "yellow"):
            button_color: color = yellow
        else:
            button_color: color = black

        button: Button = Button(self._window,
                                x=100, y=100,
                                width=button_width, height=button_height,
                                textColour=text_color, radius=20,
                                text=card.__repr__(), inactiveColour=button_color,
                                onClick=self._player.put_card, onClickParams=(card))
        self._buttons.append(button)
        return None

    def draw_players(self) -> None:
        pass

    def draw_cards(self) -> None:
        x_button: int = 100
        y_button: int = 100

    def draw_table_infos(self) -> None:
        pass

    def update_window(self, actual_player: Player) -> None:
        if (self._player == actual_player):
            pass

        return None

    def _create_player(self, name: str) -> None:
        self._player: Player = Player(name=name)
        return None

    def _menu_screen(self) -> None:
        run: bool = True
        clock: Clock = Clock()
        text_font = font.SysFont("comicsans", 40)
        text = text_font.render("Enter your name", True, text_color)
        text_x: int = self._get_x_center_of_window(text.get_width())

        textbox_width: int = 200
        textbox_height: int = 50
        textbox_x: int = self._get_x_center_of_window(textbox_width)
        textbox_y: int = 100
        textbox: TextBox = TextBox(self._window, x=textbox_x, y=textbox_y, width=textbox_width,
                                   height=textbox_height, fontSize=30, textColour=black)

        button_x: int = self._get_x_center_of_window(button_width)
        Button(self._window, x=button_x, y=170, width=button_width,
               height=40, text="Enter", textColour=text_color, fontSize=30,
               inactiveColour=black, onClick=self._create_player,
               onClickParams=(textbox.getText(),))

        while run:
            clock.tick(60)
            events = event.get()
            for event_ in events:
                if (event_.type == QUIT):
                    quit()
                    run = False

            self._window.fill(background)
            self._window.blit(text, (text_x, 50))
            pygame_widgets.update(events)
            display.update()

            if (self._player is not None):
                run = False

        return None

    def _get_x_center_of_window(self, width: int) -> int:
        return (self._window.get_width() // 2 - width // 2)

    def _get_y_center_of_window(self, height: int) -> int:
        return (self._window.get_height() // 2 - height // 2)

    def _get_center_of_window(self, width: int, height: int) -> Tuple[int, int]:
        return (self._get_x_center_of_window(width), self._get_y_center_of_window(height))

