import os.path
from typing import List, Optional

from pygame import display, font, event, QUIT, quit, Surface, image, transform
from pygame.time import Clock
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox

from ..model.Card import Card
from ..model.Color import Color
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
        self._top_card: Optional[Card] = Card(color=Color.GREEN, value=3)
        self._reverse: bool = False
        self._buy_cards: int = 0
        self._buttons: List[Button] = []
        self._window: display = display.set_mode((width, height))
        self._window_configuration(caption)
        # self._menu_screen()

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

    def _add_button(self, card: Card, x_pos: int, y_pos: int, rotate: int = 0) -> None:
        png: str = card.__repr__().lower() + ".png"
        img: Surface = image.load(os.path.join("/home/gabriel/Git/UNO/Cards", png))

        if rotate:
            img = transform.rotate(img, rotate)
            img = transform.scale(img, (128, 85))
            width, height = img.get_width(), img.get_height()
            x_pos = self._get_x_center_of_window(width)
            y_pos = 100
        else:
            width: int = img.get_width()
            height: int = img.get_height()

        button: Button = Button(self._window,
                                x=x_pos, y=y_pos,
                                width=width, height=height,
                                radius=30, image=img,
                                onClick=self._player.put_card, onClickParams=(card,))
        self._buttons.append(button)
        return None

    def draw_players(self) -> None:
        x_player: int = 10
        y_player: int = 10
        text_font = font.SysFont("comicsans", 20)
        for player in self._players:
            name = text_font.render(player.get_name(), True, text_color)
            num_cards = text_font.render(str(player.get_num_cards()), True, text_color)
            self._window.blit(name, (x_player, y_player))
            x_num_cards: int = x_player + name.get_width() // 2
            self._window.blit(num_cards, (x_num_cards, y_player + 20))
            x_player += name.get_width() + 20

        return None

    def draw_cards(self) -> None:
        x_button: int = 0
        y_button: int = 400

        for card in self._player.get_cards():
            self._add_button(card=card, x_pos=x_button, y_pos=y_button)
            x_button += 60
            if (x_button + 60 >= self._window.get_height()):
                y_button += 75
                x_button = 0
            x_button %= self._window.get_width()

        return None

    def draw_table_infos(self) -> None:
        text_font = font.SysFont("comicsans", 30)
        reverse = text_font.render(f"Reverse: {self._reverse}", True, text_color)
        buy = text_font.render(f"Value to buy: {self._buy_cards}", True, text_color)
        x_reverse = self._window.get_width() - reverse.get_width() - 10
        x_buy = self._window.get_width() - buy.get_width() - 10
        self._window.blit(reverse, (x_reverse, 80))
        self._window.blit(buy, (x_buy, 120))

        x_card, y_card = self._get_center_of_window(button_width, button_height)
        self._add_button(self._top_card, x_card, y_card, rotate=90)

        return None

    def update_window(self) -> None:
        run: bool = True
        clock: Clock = Clock()
        while run:
            clock.tick(60)
            events = event.get()
            for event_ in events:
                if (event_.type == QUIT):
                    quit()
                    run = False

            self._window.fill(background)
            self.draw_table_infos()
            self.draw_players()
            self.draw_cards()
            pygame_widgets.update(events)
            display.update()

        return None

    def _create_player(self, textbox: TextBox) -> None:
        self._player: Player = Player(name=textbox.getText())
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
        enter_button: Button = Button(self._window, x=button_x, y=170, width=button_width,
                                      height=40, text="Enter", textColour=text_color, fontSize=30,
                                      inactiveColour=black, onClick=self._create_player,
                                      onClickParams=(textbox,))

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

        enter_button.disable()
        textbox.disable()
        enter_button.hide()
        textbox.hide()
        self.update_window()

        return None

    def _get_x_center_of_window(self, width: int) -> int:
        return (self._window.get_width() // 2 - width // 2)

    def _get_y_center_of_window(self, height: int) -> int:
        return (self._window.get_height() // 2 - height // 2)

    def _get_center_of_window(self, width: int, height: int) -> Tuple[int, int]:
        return (self._get_x_center_of_window(width), self._get_y_center_of_window(height))

