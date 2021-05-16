from tkinter import *
from Player import Player


class Card:
    def __init__(self, name, windown, deck):
        self.__name = name
        self.__type = self.__get_type()
        self.__color = self.__get_color()
        self.__button = 0

    def name(self):
        return self.__name

    def type(self):
        return self.__type

    def color(self):
        return self.__color

    def button(self):
        return self.__button

    def create_button(self, windown, deck):
        self.__button = Button(windown, bg="black", relief=FLAT, bd=0, highlightthickness=0, activebackground="black",
                               state=DISABLED, text=self.__name, image=deck[self.name()+".png"])

    def __get_color(self):
        def verify(index):
            if self.__name[index] == 'r':
                return "red"
            elif self.__name[index] == 'g':
                return "green"
            elif self.__name[index] == 'b':
                return "blue"
            elif self.__name[index] == 'y':
                return "yellow"
            else:
                return "special"

        if self.__type == "reverse":
            return verify(7)
        elif self.__type == "block":
            return verify(5)
        elif self.__type == "buy" and self.__name[1] != '4':
            return verify(2)
        else:
            return verify(1)

    def __get_type(self):
        if self.__name[0] == '+':
            return "buy"
        elif self.__name[0] == 'r':
            return "reverse"
        elif self.__name[0] == 'b':
            return "block"
        elif self.__name[0] == 'c':
            return "change_color"
        else:
            return self.__name[0]

    def change_color(self, new_color):
        self.__color = new_color

    def enable_button(self):
        self.__button["state"] = NORMAL

    def disable_button(self):
        self.__button["state"] = DISABLED
