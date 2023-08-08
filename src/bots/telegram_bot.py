from typing import Coroutine
from uuid import uuid4

from telegram import (Bot, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle,
                      InlineQueryResultCachedSticker as Sticker, InputTextMessageContent, Update)
from telegram.ext import (Application, CallbackContext, ChosenInlineResultHandler, CommandHandler,
                          InlineQueryHandler)

from src.model.Card import Card
from src.model.Color import Color, COLORS
from src.model.exceptions import *
from src.model.Player import Player
from src.model.Table import Table
from src.utils.stickers import STICKERS, STICKERS_GREY
from src.utils.token import TELEGRAM


class Telegram:
    def __init__(self):
        self.application = Application.builder().token(TELEGRAM).build()
        self.games: dict[int, Table] = {}
        self.application.add_handler(InlineQueryHandler(self.show_cards))
        self.application.add_handler(ChosenInlineResultHandler(self.selected_card, ))
        # self.application.add_handler(CallbackQueryHandler(self.show_cards))
        self.application.add_handler(CommandHandler("join", self.join_game))
        self.application.add_handler(CommandHandler("leave", self.leave_game))
        self.application.add_handler(CommandHandler("skip", self.skip))
        self.application.add_handler(
            CommandHandler("start", self.start_game))
        self.application.add_handler(CommandHandler("create", self.create_game))
        self.application.add_handler(CommandHandler("change_mode", self.change_mode))
        self.application.run_polling()

    @staticmethod
    def chat_id(update: Update) -> int:
        return update.message.chat.id

    def game(self, chat_id: int) -> Table:
        try:
            return self.games[chat_id]
        except KeyError:
            raise GameNotCreated

    def create_game(self, update: Update, context: CallbackContext) -> Coroutine:
        chat_id = self.chat_id(update=update)
        self.games[chat_id] = Table()
        message: str = f"New game created! \n" \
                       f"Type /join to play!"
        return self.send_message_to_all(update=update, message=message)

    def join_game(self, update: Update, context: CallbackContext) -> Coroutine:
        player_name: str = update.message.from_user.first_name
        player_id: int = update.message.from_user.id
        player_tag: str = update.message.from_user.name
        new_player: Player = Player(name=player_name, id_=player_id, tag=player_tag)
        try:
            game = self.game(chat_id=self.chat_id(update=update))
            game.add_player(player=new_player)
            message: str = f"Joined the game!"
        except (AlreadyJoined, GameNotCreated) as e:
            message = f"{e}"

        return self.send_message_to_all(update=update, message=message)

    def leave_game(self, update: Update, context: CallbackContext) -> Coroutine:
        player_id: int = update.message.from_user.id
        game = self.game(chat_id=self.chat_id(update=update))
        player: Player = game.get_player(player_id=player_id)
        try:
            game.remove_player(player=player)
            message: str = f"Left the game!"
        except NotInGame as e:
            message = f"{e}"

        return self.send_message_to_all(update=update, message=message)

    async def start_game(self, update: Update, callback: CallbackContext) -> None:
        bot: Bot = callback.bot
        chat_id = self.chat_id(update=update)
        game = self.game(chat_id=chat_id)

        try:
            game.start_game()
        except (AttributeError, AlreadyRunning, GameNotReady) as e:
            message = f"{e}"
            await bot.send_message(chat_id, text=message)
        else:
            await bot.send_message(chat_id, text="Game started!")
            await bot.send_sticker(chat_id, sticker=STICKERS[str(game.current_card()).lower()])
            await bot.send_message(chat_id, text=game.status(),
                                   reply_markup=InlineKeyboardMarkup(self.make_choice(chat_id)))

        return None

    @staticmethod
    def make_choice(chat_id: int, text: str = "Make your choice!"
                    ) -> list[list[InlineKeyboardButton]]:
        return [
            [InlineKeyboardButton(text=text, switch_inline_query_current_chat=f"{chat_id}")]]

    async def show_cards(self, update: Update, callback: CallbackContext) -> None:
        card_buttons = []
        inline_query = update.inline_query
        user_id: int = inline_query.from_user.id
        try:
            chat_id: int = int(inline_query.query)
            game = self.game(chat_id=chat_id)
        except (KeyError, ValueError):
            return None
        current_player: Player = game.current_player()
        player: Player = game.get_player(user_id)
        if (player is None):
            return None
        if (game.choosing_color()) and (user_id == current_player.id()):
            card_buttons = self.choose_color(player=current_player)
        elif (game.ready() or game.waiting() or game.created()):
            card_buttons = self.show_settings(settings=game.settings())
        elif (user_id == current_player.id()):
            try:
                status = game.status()
            except AttributeError:
                return None
            playable_cards = game.playable_cards
            for option in game.current_player_options():
                sticker_id = option.name.lower()
                sticker = STICKERS[sticker_id]
                new_button = Sticker(sticker_id, sticker_file_id=sticker)
                card_buttons.append(new_button)
            if (current_player.not_have_playable_card(playable_cards=playable_cards)):
                if (current_player.num_cards() < 50):
                    self._disable_all_cards(card_buttons=card_buttons, player=current_player,
                                            status=status)
            else:
                self._gen_sticker_cards(card_buttons=card_buttons, player=current_player,
                                        playable_cards=playable_cards, status=status)
        else:
            self._disable_all_cards(card_buttons=card_buttons, player=player, status=status)

        bot = callback.bot
        await bot.answer_inline_query(update.inline_query.id, card_buttons, cache_time=0)
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
    async def send_message_to_all(update: Update, message: str,
                                  reply_markup: InlineKeyboardMarkup = None) -> None:
        await update.message.reply_text(message, reply_markup=reply_markup)
        return None

    async def selected_card(self, update: Update, context: CallbackContext) -> None:
        inline_result = update.chosen_inline_result
        user = inline_result.from_user
        card_name: str = inline_result.result_id
        sender_id: int = user.id
        try:
            chat_id: int = int(inline_result.query)
            game = self.game(chat_id=chat_id)
        except (KeyError, ValueError):
            return None
        current_player: Player = game.current_player()
        try:
            card_name: Color = Color[card_name]
        except KeyError:
            if (card_name not in STICKERS.keys()):
                try:
                    game.change_mode(setting=card_name)
                except SyntaxError:
                    pass
                return None

        if (current_player.id() == sender_id):
            if isinstance(card_name, Color):
                selected: Color = card_name
            else:
                selected: Card = current_player.select_card(name=card_name)
            game.turn(selected=selected)
            bot = context.bot
            if (game.terminated()):
                await bot.send_message(chat_id,
                                       text=f"Game ended, {game.current_player()} won!")
            else:
                await bot.send_message(chat_id, text=game.status(),
                                       reply_markup=InlineKeyboardMarkup(self.make_choice(chat_id)))

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

    @staticmethod
    def show_settings(settings: list[tuple[str, bool]]) -> list[InlineQueryResultArticle]:
        articles: list[InlineQueryResultArticle] = []
        for setting, value in settings:
            message = f"Setting {setting} changed to {not value}."
            new_article = InlineQueryResultArticle(id=setting, title=f"{setting} ({value})",
                                                   input_message_content=InputTextMessageContent(
                                                       message))
            articles.append(new_article)
        return articles

    async def change_mode(self, update: Update, context: CallbackContext) -> None:
        bot = context.bot
        chat_id = self.chat_id(update=update)
        game = self.game(chat_id=chat_id)
        try:
            new_mode: int = int(context.args[0])
            game.change_mode(new_mode)
        except (IndexError, ValueError):
            await bot.send_message(chat_id, text="Click the button to modify a setting!",
                                   reply_markup=InlineKeyboardMarkup(
                                       self.make_choice(chat_id, "Choose setting!")))
        else:
            await bot.send_message(chat_id, text=f"Game changed to mode {new_mode}.")
        return None

    async def skip(self, update: Update, context: CallbackContext) -> None:
        bot = context.bot
        chat_id = self.chat_id(update=update)
        game = self.game(chat_id=chat_id)
        if (game.running()):
            game.skip()
        await bot.send_message(chat_id, text=game.status(),
                               reply_markup=InlineKeyboardMarkup(self.make_choice(chat_id)))
        return None
