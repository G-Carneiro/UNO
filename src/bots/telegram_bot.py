from typing import List, Optional
from uuid import uuid4

from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup,
                      Bot, InlineQueryResultCachedSticker, InputTextMessageContent)
from telegram.ext import (CallbackContext, CommandHandler, Updater,
                          InlineQueryHandler, ChosenInlineResultHandler)

from src.model.Card import Card
from src.model.Player import Player
from src.model.Table import Table

updater: Updater = Updater("5354446808:AAEL1YJKk8Vjl7zbsU-RpX2q8f3G87eOjCA")
dispatcher = updater.dispatcher
table: Optional[Table] = None
chat_id: Optional[int] = None

STICKERS = {
    '0blue': 'BQADBAAD2QEAAl9XmQAB--inQsYcLTsC',
    '1blue': 'BQADBAAD2wEAAl9XmQABBzh4U-rFicEC',
    '2blue': 'BQADBAAD3QEAAl9XmQABo3l6TT0MzKwC',
    '3blue': 'BQADBAAD3wEAAl9XmQAB2y-3TSapRtIC',
    '4blue': 'BQADBAAD4QEAAl9XmQABT6nhOuolqKYC',
    '5blue': 'BQADBAAD4wEAAl9XmQABwRfmekGnpn0C',
    '6blue': 'BQADBAAD5QEAAl9XmQABQITgUsEsqxsC',
    '7blue': 'BQADBAAD5wEAAl9XmQABVhPF6EcfWjEC',
    '8blue': 'BQADBAAD6QEAAl9XmQABP6baig0pIvYC',
    '9blue': 'BQADBAAD6wEAAl9XmQAB0CQdsQs_pXIC',
    '+2blue': 'BQADBAAD7QEAAl9XmQAB00Wii7R3gDUC',
    'blockblue': 'BQADBAAD8QEAAl9XmQAB_RJHYKqlc-wC',
    'reverseblue': 'BQADBAAD7wEAAl9XmQABo7D0B9NUPmYC',
    '0green': 'BQADBAAD9wEAAl9XmQABb8CaxxsQ-Y8C',
    '1green': 'BQADBAAD-QEAAl9XmQAB9B6ti_j6UB0C',
    '2green': 'BQADBAAD-wEAAl9XmQABYpLjOzbRz8EC',
    '3green': 'BQADBAAD_QEAAl9XmQABKvc2ZCiY-D8C',
    '4green': 'BQADBAAD_wEAAl9XmQABJB52wzPdHssC',
    '5green': 'BQADBAADAQIAAl9XmQABp_Ep1I4GA2cC',
    '6green': 'BQADBAADAwIAAl9XmQABaaMxxa4MihwC',
    '7green': 'BQADBAADBQIAAl9XmQABv5Q264Crz8gC',
    '8green': 'BQADBAADBwIAAl9XmQABjMH-X9UHh8sC',
    '9green': 'BQADBAADCQIAAl9XmQAB26fZ2fW7vM0C',
    '+2green': 'BQADBAADCwIAAl9XmQAB64jIZrgXrQUC',
    'blockgreen': 'BQADBAADDwIAAl9XmQAB17yhhnh46VQC',
    'reversegreen': 'BQADBAADDQIAAl9XmQAB_xcaab0DkegC',
    '0red': 'BQADBAADEQIAAl9XmQABiUfr1hz-zT8C',
    '1red': 'BQADBAADEwIAAl9XmQAB5bWfwJGs6Q0C',
    '2red': 'BQADBAADFQIAAl9XmQABHR4mg9Ifjw0C',
    '3red': 'BQADBAADFwIAAl9XmQABYBx5O_PG2QIC',
    '4red': 'BQADBAADGQIAAl9XmQABTQpGrlvet3cC',
    '5red': 'BQADBAADGwIAAl9XmQABbdLt4gdntBQC',
    '6red': 'BQADBAADHQIAAl9XmQABqEI274p3lSoC',
    '7red': 'BQADBAADHwIAAl9XmQABCw8u67Q4EK4C',
    '8red': 'BQADBAADIQIAAl9XmQAB8iDJmLxp8ogC',
    '9red': 'BQADBAADIwIAAl9XmQAB_HCAww1kNGYC',
    '+2red': 'BQADBAADJQIAAl9XmQABuz0OZ4l3k6MC',
    'blockred': 'BQADBAADKQIAAl9XmQAC2AL5Ok_ULwI',
    'reversered': 'BQADBAADJwIAAl9XmQABu2tIeQTpDvUC',
    '0yellow': 'BQADBAADKwIAAl9XmQAB_nWoNKe8DOQC',
    '1yellow': 'BQADBAADLQIAAl9XmQABVprAGUDKgOQC',
    '2yellow': 'BQADBAADLwIAAl9XmQABqyT4_YTm54EC',
    '3yellow': 'BQADBAADMQIAAl9XmQABGC-Xxg_N6fIC',
    '4yellow': 'BQADBAADMwIAAl9XmQABbc-ZGL8kApAC',
    '5yellow': 'BQADBAADNQIAAl9XmQAB67QJZIF6XAcC',
    '6yellow': 'BQADBAADNwIAAl9XmQABJg_7XXoITsoC',
    '7yellow': 'BQADBAADOQIAAl9XmQABVrd7OcS2k34C',
    '8yellow': 'BQADBAADOwIAAl9XmQABRpJSahBWk3EC',
    '9yellow': 'BQADBAADPQIAAl9XmQAB9MwJWKLJogYC',
    '+2yellow': 'BQADBAADPwIAAl9XmQABaPYK8oYg84cC',
    'blockyellow': 'BQADBAADQwIAAl9XmQABO_AZKtxY6IMC',
    'reverseyellow': 'BQADBAADQQIAAl9XmQABZdQFahGG6UQC',
    '+4': 'BQADBAAD9QEAAl9XmQABVlkSNfhn76cC',
    'change_color': 'BQADBAAD8wEAAl9XmQABl9rUOPqx4E4C',
    'option_draw': 'BQADBAAD-AIAAl9XmQABxEjEcFM-VHIC',
    'option_pass': 'BQADBAAD-gIAAl9XmQABcEkAAbaZ4SicAg',
    'option_bluff': 'BQADBAADygIAAl9XmQABJoLfB9ntI2UC',
    'option_info': 'BQADBAADxAIAAl9XmQABC5v3Z77VLfEC'
}


def create_game(update: Update, context: CallbackContext) -> None:
    global table
    table = Table()
    message: str = f"New game created! \n" \
                   f"Type /join_game to play!"
    send_message_to_all(update=update, message=message)
    return None


def join_game(update: Update, context: CallbackContext) -> None:
    player_name: str = update.message.from_user.full_name
    player_id: int = update.message.from_user.id
    new_player: Player = Player(name=player_name, id_=player_id)
    if (new_player not in table.get_players()):
        table.add_player(player=new_player)
        message: str = f"{player_name} joined the game!"
    else:
        message = f"Already in game!"

    # table.add_player(player=new_player)
    # message: str = f"{player_name} joined the game!"
    send_message_to_all(update=update, message=message)
    return None


def start_game(update: Update, callback: CallbackContext) -> None:
    bot: Bot = update.message.bot
    chat = update.message.chat
    global chat_id
    chat_id = chat.id

    if (table is None):
        bot.send_message(chat_id, text="First, create a game!")
        return None
    elif (len(table.get_players()) < 2):
        bot.send_message(chat_id, text="Wait more players!")
        return None

    table.start_game()
    current_player: Player = table.current_player()
    message: str = f"Game started! \n" \
                   f"Current card is {table.current_card()}. \n" \
                   f"Players are {table.get_players()}. \n" \
                   f"First player is {current_player}. \n"
    # send_message_to_all(update=update, message=message)
    bot.send_sticker(chat_id, sticker=STICKERS[str(table.current_card()).lower()])
    bot.send_message(chat_id, text=message, reply_markup=InlineKeyboardMarkup(make_choice()))

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
    added_cards: List[str] = []
    if (user_id == current_player.id()):
        for card in sorted(player.get_cards()):
            card_name: str = str(card).lower()
            if (card_name in added_cards):
                sticker_id: str = str(uuid4())
                input_message = InputTextMessageContent(status())
            else:
                sticker_id = card_name
                added_cards.append(card_name)
                input_message = None

            new_button = InlineQueryResultCachedSticker(sticker_id, sticker_file_id=STICKERS[card_name],
                                                        input_message_content=input_message)
            card_buttons.append(new_button)
    else:
        input_message = InputTextMessageContent(status())
        for card in sorted(player.get_cards()):
            card_name: str = str(card).lower()
            sticker_id: str = str(uuid4())
            new_sticker = InlineQueryResultCachedSticker(sticker_id, sticker_file_id=STICKERS[card_name],
                                                         input_message_content=input_message)
            card_buttons.append(new_sticker)

    # bot.send_message(chat.id, text="Make your choice!", reply_markup=card_buttons)
    updater.bot.answer_inline_query(update.inline_query.id, card_buttons)
    return None


def send_message_to_all(update: Update, message: str,
                        reply_markup: InlineKeyboardMarkup = None) -> None:
    if reply_markup is None:
        update.message.reply_text(message)
    else:
        update.message.reply_text(message, reply_markup=reply_markup)
    return None


def selected_card(update: Update, context: CallbackContext) -> None:
    current_player: Player = table.current_player()
    inline_result = update.chosen_inline_result
    user = inline_result.from_user
    card_name: str = inline_result.result_id
    if (card_name not in STICKERS.keys()):
        return None
    sender_id: int = user.id
    if (current_player.id() == sender_id):
        card: Card = current_player.select_card(name=card_name)
        played: bool = table.turn(card=card)
        if played:
            # send_message_to_all(update=update, message=status())
            updater.bot.send_message(chat_id, text=status(), reply_markup=InlineKeyboardMarkup(make_choice()))
            # show_cards()

    return None


def status() -> str:
    current_status: str = f"Current card is {table.current_card()}. \n" \
                          f"Current player is {table.current_player()} \n" \
                          f"Next players {table.get_players()}."
    return current_status


dispatcher.add_handler(InlineQueryHandler(show_cards))
dispatcher.add_handler(ChosenInlineResultHandler(selected_card, pass_job_queue=True))
# dispatcher.add_handler(CallbackQueryHandler(show_cards))
dispatcher.add_handler(CommandHandler("join_game", join_game))
dispatcher.add_handler(CommandHandler("start_game", start_game, pass_args=True, pass_job_queue=True))
dispatcher.add_handler(CommandHandler("create_game", create_game))
updater.start_polling()
updater.idle()
