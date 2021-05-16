from Card import Card
from Player import Player
from random import randint, choice, shuffle
import os

cards_selection = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "reverse", "block", "+2", "special")
colors = ("green", "red", "blue", "yellow")
special = ("change_color", "+4")
initial_cards_number = 7


class Game:
    def __init__(self, num_players, windown, deck):
        self.__num_players = num_players
        self.__reverse = False
        self.__end_game = False
        self.__cards = []
        self.__top_card = self.__game_configuration(windown, deck)
        self.__buy_cards = 0
        self.__players = []

    def num_players(self):
        return self.__num_players

    def players(self):
        return self.__players

    def reverse(self):
        return self.__reverse

    def __change_reverse(self):
        self.__reverse = not self.__reverse

    def top_card(self):
        return self.__top_card

    def __change_top(self, new_top):
        if new_top == 0:
            self.__buy_cards = 0
            return
        else:
            self.__top_card = new_top
            self.__top_verify()
        
    def buy_cards(self):
        return self.__buy_cards

    def __reset_buy(self):
        self.__buy_cards = 0

    def __add_buy(self, value):
        self.__buy_cards += value

    def __game_configuration(self, windown, deck):
        name = randint(0, 9)
        name = cards_selection[name] + choice(colors)
        teste = os.listdir('Cards')
        for i in range(len(teste)):
            size = len(teste[i]) - 4
            self.__cards.append(Card(teste[i][0:size], windown, deck))

        del teste
        for i in range(len(self.__cards)):
            if name == self.__cards[i].name():
                return self.__cards[i]

        return None

    def create_game(self, windown):
        for i in range(self.__num_players):
            name = i # input(f"Digite o nome do jogador {i}: ")
            self.__players.append(Player(name))
            for j in range(initial_cards_number):
                self.__players[i].buy_card(self.__cards, windown)

        self.__init_game()

    def __init_game(self):
        shuffle(self.__players)
        for i in range(len(self.__players)):
            self.__players[i].change_id(i)

        next_player = 0
        while not self.__end_game:
            actual_player = self.__players[next_player]
            self.__change_top(actual_player.play(self.buy_cards(), self.top_card(), self.__cards))
            if len(actual_player.cards()) == 0:
                self.end_game(actual_player.name())

            next_player = self.__next_player(actual_player.id())

    def new_round(self):
        for i in range(len(self.__players)):
            self.__players[i].reset_cards()
            for j in range(initial_cards_number):
                self.__players[i].buy_card()

        self.__init_game()

    def stats_game(self):
        print("Game Stats")
        print("Player : Cards")
        for i in range(len(self.__players)):
            print(f"{self.__players[i].id()} : {(self.__players[i].cards())}")

    def end_game(self, winner_player):
        self.__end_game = True
        print(f"Fim de jogo. \n"
              f"{winner_player} venceu!!!")

    def __next_player(self, actual_player):
        next_player = actual_player

        if self.top_card().type() == "block":
            if self.reverse():
                next_player -= 2
            else:
                next_player += 2
        else:
            if self.reverse():
                next_player -= 1
            else:
                next_player += 1

        next_player %= self.num_players()
        return next_player

    def __top_verify(self):
        if self.top_card().type() == "reverse":
            self.__change_reverse()
        elif self.top_card().type() == "buy":
            self.__buy_cards += int(self.__top_card.name()[1])
        elif self.top_card().type() == "block":
            self.__buy_cards = 0
