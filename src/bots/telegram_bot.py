from typing import List, Optional, Set
from uuid import uuid4

from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup,
                      Bot, InlineQueryResultCachedSticker as Sticker,
                      InputTextMessageContent, InlineQueryResultArticle)
from telegram.ext import (CallbackContext, CommandHandler, Updater,
                          InlineQueryHandler, ChosenInlineResultHandler)

from src.model.Card import Card
from src.model.Color import Color, COLORS
from src.model.Player import Player
from src.model.Table import Table
from src.utils.stickers import STICKERS, STICKERS_GREY
from src.utils.token import TOKEN

updater: Updater = Updater(TOKEN)
dispatcher = updater.dispatcher
table: Optional[Table] = None
chat_id: Optional[int] = None


def create_game(update: Update, context: CallbackContext) -> None:
    global table
    table = Table()
    message: str = f"New game created! \n" \
                   f"Type /join_game to play!"
    send_message_to_all(update=update, message=message)
    return None


def join_game(update: Update, context: CallbackContext) -> None:
    player_name: str = update.message.from_user.first_name
    player_id: int = update.message.from_user.id
    new_player: Player = Player(name=player_name, id_=player_id)
    if (new_player not in table.get_players()):
        table.add_player(player=new_player)
        message: str = f"Joined the game!"
    else:
        message = f"Already in game!"

    # table.add_player(player=new_player)
    # message: str = f"{player_name} joined the game!"
    send_message_to_all(update=update, message=message)
    return None


def start_game(update: Update, callback: CallbackContext) -> None:
    bot: Bot = callback.bot
    chat = update.message.chat
    global chat_id
    chat_id = chat.id

    if (table is None):
        bot.send_message(chat_id, text="First, create a game!")
        return None
    elif (not table.ready()):
        bot.send_message(chat_id, text="Wait more players!")
        return None
    elif (table.running()):
        bot.send_message(chat_id, text="Game already started!")

    table.start_game()
    bot.send_message(chat_id, text="Game started!")
    bot.send_sticker(chat_id, sticker=STICKERS[str(table.current_card()).lower()])
    bot.send_message(chat_id, text=status(), reply_markup=InlineKeyboardMarkup(make_choice()))

    return None


def make_choice() -> List[List[InlineKeyboardButton]]:
    return [[InlineKeyboardButton(text="Make your choice!", switch_inline_query_current_chat='')]]


def show_cards(update: Update, callback: CallbackContext) -> None:
    card_buttons = []
    current_player: Player = table.current_player()
    user_id: int = update.inline_query.from_user.id
    player: Player = table.get_player(user_id)
    if (player is None):
        return None

    if (table.choosing_color()) and (user_id == current_player.id()):
        card_buttons = choose_color()
    elif (user_id == current_player.id()):
        playable_cards = table.playable_cards
        if (not current_player.have_allowed_card(allowed_cards=playable_cards)):
            sticker_id = "option_draw"
            sticker = STICKERS[sticker_id]
            new_button = Sticker(sticker_id, sticker_file_id=sticker)
            card_buttons.append(new_button)
            _disable_all_cards(card_buttons=card_buttons, player=current_player)
        else:
            _gen_sticker_cards(card_buttons=card_buttons, player=current_player,
                               playable_cards=playable_cards)
    else:
        _disable_all_cards(card_buttons=card_buttons, player=player)

    bot = callback.bot
    # dispatcher.run_async(bot.answer_inline_query, update.inline_query.id, card_buttons, cache_time=0)
    bot.answer_inline_query(update.inline_query.id, card_buttons, cache_time=0)
    return None


def _gen_sticker_cards(card_buttons: List[Sticker], player: Player, playable_cards: Set[Card]) -> None:
    added_cards: List[str] = []
    for card in sorted(player.get_cards()):
        card_name: str = str(card).lower()
        if (card_name in added_cards) or (card not in playable_cards):
            sticker_id: str = str(uuid4())
            sticker = STICKERS_GREY[card_name]
            input_message = InputTextMessageContent(status())
        else:
            sticker_id = card_name
            sticker = STICKERS[card_name]
            added_cards.append(card_name)
            input_message = None

        new_button = Sticker(sticker_id, sticker_file_id=sticker,
                             input_message_content=input_message)
        card_buttons.append(new_button)
    return None


def _disable_all_cards(card_buttons: List[Sticker], player: Player) -> None:
    input_message = InputTextMessageContent(status())
    for card in sorted(player.get_cards()):
        card_name: str = str(card).lower()
        sticker_id: str = str(uuid4())
        sticker = STICKERS_GREY[card_name]
        new_sticker = Sticker(sticker_id, sticker_file_id=sticker,
                              input_message_content=input_message)
        card_buttons.append(new_sticker)

    return None


def send_message_to_all(update: Update, message: str,
                        reply_markup: InlineKeyboardMarkup = None) -> None:
    update.message.reply_text(message, reply_markup=reply_markup)
    return None


def selected_card(update: Update, context: CallbackContext) -> None:
    current_player: Player = table.current_player()
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
        table.turn(selected=selected)
        bot = context.bot
        if (table.terminated()):
            bot.send_message(chat_id, text=f"Game ended, {table.current_player()} won!")
        else:
            bot.send_message(chat_id, text=status(),
                             reply_markup=InlineKeyboardMarkup(make_choice()))

    return None


def status() -> str:
    return table.status()


def choose_color() -> List[InlineQueryResultArticle]:
    colors: List[InlineQueryResultArticle] = []
    for color in COLORS:
        message: str = str(color)
        num_cards: int = table.current_player().num_color_card(color)
        new_article = InlineQueryResultArticle(id=color.name, title=f"{message} ({num_cards})",
                                               input_message_content=InputTextMessageContent(message))
        colors.append(new_article)

    return colors


# TODO: mark actual player in chat
dispatcher.add_handler(InlineQueryHandler(show_cards))
dispatcher.add_handler(ChosenInlineResultHandler(selected_card, pass_job_queue=True))
# dispatcher.add_handler(CallbackQueryHandler(show_cards))
dispatcher.add_handler(CommandHandler("join_game", join_game))
dispatcher.add_handler(CommandHandler("start_game", start_game, pass_args=True, pass_job_queue=True))
dispatcher.add_handler(CommandHandler("create_game", create_game))
updater.start_polling()
updater.idle()
