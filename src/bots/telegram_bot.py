from typing import Dict
from uuid import uuid4

from telegram import (Bot, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle,
                      InlineQueryResultCachedSticker as Sticker, InputTextMessageContent, Update)
from telegram.ext import (CallbackContext, ChosenInlineResultHandler, CommandHandler,
                          InlineQueryHandler, Updater)

from src.model.Card import Card
from src.model.Color import Color, COLORS
from src.model.exceptions import *
from src.model.Player import Player
from src.model.Table import Table
from src.utils.stickers import STICKERS, STICKERS_GREY
from src.utils.token import TELEGRAM


class Telegram:
    def __init__(self):
        self.updater: Updater = Updater(TELEGRAM)
        self.dispatcher = self.updater.dispatcher
        self.table: Dict[int, Table] = {}
        # self.chat_id: Optional[int] = None
        self.dispatcher.add_handler(InlineQueryHandler(self.show_cards))
        self.dispatcher.add_handler(ChosenInlineResultHandler(self.selected_card,
                                                              pass_job_queue=True))
        # dispatcher.add_handler(CallbackQueryHandler(show_cards))
        self.dispatcher.add_handler(CommandHandler("join", self.join_game))
        self.dispatcher.add_handler(CommandHandler("leave", self.leave_game))
        self.dispatcher.add_handler(CommandHandler("skip", self.skip))
        self.dispatcher.add_handler(
            CommandHandler("start", self.start_game, pass_args=True, pass_job_queue=True))
        self.dispatcher.add_handler(CommandHandler("create", self.create_game))
        self.updater.start_polling()
        self.updater.idle()

    @staticmethod
    def chat_id(update: Update) -> int:
        return update.message.chat.id

    def game(self, update: Update) -> Table:
        chat_id = self.chat_id(update=update)
        try:
            return self.table[chat_id]
        except KeyError:
            raise GameNotCreated

    def create_game(self, update: Update, context: CallbackContext) -> None:
        chat_id = self.chat_id(update=update)
        self.table[chat_id] = Table()
        message: str = f"New game created! \n" \
                       f"Type /join to play!"
        self.send_message_to_all(update=update, message=message)
        return None

    def join_game(self, update: Update, context: CallbackContext) -> None:
        player_name: str = update.message.from_user.first_name
        player_id: int = update.message.from_user.id
        new_player: Player = Player(name=player_name, id_=player_id)
        try:
            game = self.game(update=update)
            game.add_player(player=new_player)
            message: str = f"Joined the game!"
        except (AlreadyJoined, GameNotCreated) as e:
            message = f"{e}"

        self.send_message_to_all(update=update, message=message)
        return None

    def leave_game(self, update: Update, context: CallbackContext) -> None:
        player_id: int = update.message.from_user.id
        game = self.game(update=update)
        player: Player = game.get_player(player_id=player_id)
        try:
            game.remove_player(player=player)
            message: str = f"Left the game!"
        except NotInGame as e:
            message = f"{e}"

        self.send_message_to_all(update=update, message=message)
        return None

    def start_game(self, update: Update, callback: CallbackContext) -> None:
        bot: Bot = callback.bot
        chat_id = self.chat_id(update=update)
        game = self.game(update=update)

        try:
            game.start_game()
        except (AttributeError, AlreadyRunning, GameNotReady) as e:
            message = f"{e}"
            bot.send_message(chat_id, text=message)
        else:
            bot.send_message(chat_id, text="Game started!")
            bot.send_sticker(chat_id, sticker=STICKERS[str(game.current_card()).lower()])
            bot.send_message(chat_id, text=game.status(),
                             reply_markup=InlineKeyboardMarkup(self.make_choice()))

        return None

    @staticmethod
    def make_choice() -> list[list[InlineKeyboardButton]]:
        return [
            [InlineKeyboardButton(text="Make your choice!", switch_inline_query_current_chat='')]]

    def show_cards(self, update: Update, callback: CallbackContext) -> None:
        card_buttons = []
        game = self.game(update=update)
        current_player: Player = game.current_player()
        user_id: int = update.inline_query.from_user.id
        player: Player = game.get_player(user_id)
        if (player is None):
            return None

        status = game.status()
        if (game.choosing_color()) and (user_id == current_player.id()):
            card_buttons = self.choose_color(player=current_player)
        elif (user_id == current_player.id()):
            playable_cards = game.playable_cards
            if (game.call_bluff):
                sticker_id = "call_bluff"
                sticker = STICKERS[sticker_id]
                new_button = Sticker(sticker_id, sticker_file_id=sticker)
                card_buttons.append(new_button)
            if (current_player.not_have_playable_card(playable_cards=playable_cards)):
                sticker_id = "draw"
                sticker = STICKERS[sticker_id]
                new_button = Sticker(sticker_id, sticker_file_id=sticker)
                card_buttons.append(new_button)
                if (current_player.num_cards() < 50):
                    self._disable_all_cards(card_buttons=card_buttons, player=current_player,
                                            status=status)
            else:
                self._gen_sticker_cards(card_buttons=card_buttons, player=current_player,
                                        playable_cards=playable_cards, status=status)
        else:
            self._disable_all_cards(card_buttons=card_buttons, player=player, status=status)

        bot = callback.bot
        bot.answer_inline_query(update.inline_query.id, card_buttons, cache_time=0)
        return None

    @staticmethod
    def _gen_sticker_cards(card_buttons: list[Sticker], player: Player,
                           playable_cards: set[Card], status: str) -> None:
        added_cards: list[str] = []
        for card in player.get_cards():
            card_name: str = str(card).lower()
            if (card_name in added_cards) or (card not in playable_cards):
                if (player.num_cards() > 50):
                    continue
                sticker_id: str = str(uuid4())
                sticker = STICKERS_GREY[card_name]
                input_message = InputTextMessageContent(status)
            else:
                sticker_id = card_name
                sticker = STICKERS[card_name]
                added_cards.append(card_name)
                input_message = None

            new_button = Sticker(sticker_id, sticker_file_id=sticker,
                                 input_message_content=input_message)
            card_buttons.append(new_button)
        return None

    @staticmethod
    def _disable_all_cards(card_buttons: list[Sticker], player: Player, status: str) -> None:
        input_message = InputTextMessageContent(status)
        for card in player.get_cards():
            card_name: str = str(card).lower()
            sticker_id: str = str(uuid4())
            sticker = STICKERS_GREY[card_name]
            new_sticker = Sticker(sticker_id, sticker_file_id=sticker,
                                  input_message_content=input_message)
            card_buttons.append(new_sticker)

        return None

    @staticmethod
    def send_message_to_all(update: Update, message: str,
                            reply_markup: InlineKeyboardMarkup = None) -> None:
        update.message.reply_text(message, reply_markup=reply_markup)
        return None

    def selected_card(self, update: Update, context: CallbackContext) -> None:
        game = self.game(update=update)
        current_player: Player = game.current_player()
        inline_result = update.chosen_inline_result
        user = inline_result.from_user
        card_name: str = inline_result.result_id
        try:
            card_name: Color = Color[card_name]
        except KeyError:
            if (card_name not in STICKERS.keys()):
                return None

        sender_id: int = user.id
        if (current_player.id() == sender_id):
            if isinstance(card_name, Color):
                selected: Color = card_name
            else:
                selected: Card = current_player.select_card(name=card_name)
            game.turn(selected=selected)
            bot = context.bot
            chat_id = self.chat_id(update=update)
            if (game.terminated()):
                bot.send_message(chat_id,
                                 text=f"Game ended, {game.current_player()} won!")
            else:
                bot.send_message(chat_id, text=game.status(),
                                 reply_markup=InlineKeyboardMarkup(self.make_choice()))

        return None

    @staticmethod
    def choose_color(player: Player) -> list[InlineQueryResultArticle]:
        colors: list[InlineQueryResultArticle] = []
        for color in COLORS:
            message: str = str(color)
            num_cards: int = player.num_color_card(color)
            new_article = InlineQueryResultArticle(id=color.name, title=f"{message} ({num_cards})",
                                                   input_message_content=InputTextMessageContent(
                                                       message))
            colors.append(new_article)

        return colors

    def skip(self, update: Update, context: CallbackContext) -> None:
        bot = context.bot
        game = self.game(update=update)
        if (game.running()):
            game.skip()
        bot.send_message(self.chat_id, text=game.status(),
                         reply_markup=InlineKeyboardMarkup(self.make_choice()))
        return None


# TODO: mark actual player in chat

# dispatcher.add_handler(InlineQueryHandler(show_cards))
# dispatcher.add_handler(ChosenInlineResultHandler(selected_card, pass_job_queue=True))
# # dispatcher.add_handler(CallbackQueryHandler(show_cards))
# dispatcher.add_handler(CommandHandler("join", join_game))
# dispatcher.add_handler(CommandHandler("leave", leave_game))
# dispatcher.add_handler(CommandHandler("skip", skip))
# dispatcher.add_handler(CommandHandler("start", start_game, pass_args=True, pass_job_queue=True))
# dispatcher.add_handler(CommandHandler("create", create_game))
# updater.start_polling()
# updater.idle()
Telegram()
