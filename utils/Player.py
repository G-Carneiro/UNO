from random import randint, choice, shuffle
from time import sleep
from tkinter import *
from functools import partial
#from Card import Card
from copy import deepcopy


cards_selection = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "reverse", "block", "+2", "special")
colors = ("green", "red", "blue", "yellow")
special = ("change_color", "+4")


class Player:
    def __init__(self, name):
        self.__name = name
        self.__cards = []
        self.__uno = False
        self.__id = None

    def name(self):
        return self.__name

    def buy_card(self, cards, windown):
        type = randint(0, 13)
        card = cards_selection[type]
        if type < 13:
            card += choice(colors)
        else:
            card = choice(special)

        for i in range(len(cards)):
            if card == cards[i].name():
                print(id(cards[i]))
                #card = deepcopy(cards[i])
                card = cards[i]
                print(id(card))
                card.create_button(windown, cards)
                card.button()["command"] = partial(self.select_card, card.button())
                self.__cards.append(card)
                return

    def drop_card(self, top_card, buy_cards):
        """selected_card = int(input("Qual carta deseja jogar? "))
        if buy_cards == 0:
            while self.__cards[selected_card].type() != top_card.type() and \
                    self.__cards[selected_card].color() != top_card.color() and \
                    self.__cards[selected_card].color() != "special":
                selected_card = int(input("Carta inválida. Selecione outra."))
        elif buy_cards <= 10:
            while self.__cards[selected_card].type() != "block" and \
                    self.__cards[selected_card].type() != "reverse" \
                    and self.__cards[selected_card].type() != "buy":
                selected_card = int(input("Carta inválida. Selecione outra."))
        else:
            while self.__cards[selected_card].type() != "reverse" \
                    and self.__cards[selected_card].type() != "buy":
                selected_card = int(input("Carta inválida. Selecione outra."))

        selected_card = self.__cards[selected_card]

        self.remove_card(selected_card)
        if selected_card.color() == "special":
            print("Escolha uma cor: \n")
            for i in range(len(colors)):
                print(f"{i} : {colors[i]}")
            selected_card.change_color(colors[int(input())])
        if len(self.__cards) == 1:
            self.__uno = True

        return selected_card"""

    def cards(self):
        return self.__cards

    def reset_cards(self):
        self.__cards = []

    def select_card(self, button):
        for i in range(len(self.__cards)):
            if button["text"] == self.__cards[i].name():
                return self.__cards[i]

    def remove_card(self, card):
        self.__cards.remove(card)

    def uno(self):
        return self.__uno

    def id(self):
        return self.__id

    def change_id(self, new_id):
        self.__id = new_id

    def play(self, buy_cards, top_card, cards, windown):
        self.show_player(top_card)
        self.show_cards()
        if self.available_card(buy_cards, top_card):
            return self.drop_card(top_card, buy_cards)
        else:
            if buy_cards == 0:
                buy_cards = 1
            for i in range(buy_cards):
                self.buy_card(cards, windown)

            print(f"Sem carta disponível. \n"
                  f"Comprou {buy_cards} carta(s)!!!")
            sleep(3)
            return 0

    def available_card(self, buy_cards, top_card):
        if buy_cards == 0:
            available = [top_card.color(), top_card.type(), "special"]
        elif buy_cards <= 10:
            available = ["block", "reverse", "buy"]
        else:
            available = ["reverse", "buy"]

        # print(available)
        available_test = False
        for i in range(len(self.__cards)):
            for j in range(len(available)):
                if self.__cards[i].color() == available[j] or self.__cards[i].type() == available[j]:
                    self.__cards[i].enable_button()
                    available_test = True
                else:
                    self.__cards[i].disable_button()

        return available_test

    def show_cards(self):
        self.__cards.sort(key=lambda x: (len(x.color()), x.type()))
        columns = 20
        num_cards = len(self.__cards)

        for i in range(num_cards):
            self.__cards[i].button().place(x=125+(i % columns)*150, y=750+int(i / columns)*75)

    def show_player(self, top_card):
        print(f"\n \nCarta da mesa: {top_card.name()} \n"
              f"Player : {self.__name}")

    def enable_cards(self):
        for i in range(len(self.__cards)):
            self.__cards[i].enable_button()

    def disable_cards(self):
        for i in range(len(self.__cards)):
            self.__cards[i].enable_button()



