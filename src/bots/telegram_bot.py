from typing import List

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, \
    InlineQueryResultCachedSticker, Bot, InlineQueryResultCachedSticker, InputTextMessageContent
from telegram.ext import CallbackContext, CommandHandler, Updater, InlineQueryHandler, ChosenInlineResultHandler

from src.model.Player import Player
from src.model.Table import Table

updater: Updater = Updater("5354446808:AAEL1YJKk8Vjl7zbsU-RpX2q8f3G87eOjCA")
dispatcher = updater.dispatcher
table = Table()


def start(update: Update, context: CallbackContext) -> None:
    message: str = "Hi this is a test! \n" \
                   "Type /help for more information."
    update.message.reply_text(message)
    return None


def create_game(update: Update, context: CallbackContext) -> None:
    pass


def join_game(update: Update, context: CallbackContext) -> None:
    player_name: str = update.message.from_user.first_name
    message: str = f"{player_name} joined the game!"
    new_player: Player = Player(name=player_name)
    table.add_player(player=new_player)
    send_message_to_all(update=update, message=message)
    return None


def start_game(update: Update, callback: CallbackContext) -> None:
    table.start_game()
    chat = update.message.chat
    bot: Bot = update.message.bot
    current_player: Player = table._actual_player_node.data()
    message: str = f"Game started! \n" \
                   f"Current card is {table._top_card}. \n" \
                   f"Players are {table._players_list}. \n" \
                   f"First player is {current_player}. \n"
    send_message_to_all(update=update, message=message)

    card_buttons: List[InlineQueryResultCachedSticker] = []
    for card in current_player.get_cards():
        new_button = InlineQueryResultCachedSticker(id=str(card), sticker_file_id=f".../Cards/{str(card).lower()}",
                                                    input_message_content=InputTextMessageContent(str(card)))
        card_buttons.append(new_button)
    # bot.send_message(chat.id, text="Make your choice!", reply_markup=card_buttons)
    choice = [[InlineKeyboardButton(text=("Make your choice!"), switch_inline_query_current_chat='')]]
    bot.send_message(chat.id, text="Message here!", reply_markup=InlineKeyboardMarkup(card_buttons))
    # bot.answerInlineQuery(update.inline_query.id, card_buttons, cache_time=0,
    #                       switch_pm_text="switch", switch_pm_parameter='select')

    return None


def send_message_to_all(update: Update, message: str) -> None:
    update.message.reply_text(message)
    return None


def reply_to_query():
    pass


def process_result():
    pass


def city(update: Update, context):
    list_of_cities = ['Erode','Coimbatore','London', 'Thunder Bay', 'California']
    button_list = []
    for each in list_of_cities:
        button_list.append(InlineKeyboardButton(each, callback_data = each))
    reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1)) #n_cols = 1 is for single column and mutliple rows
    bot = update.message.bot
    bot.send_message(chat_id=update.message.chat_id, text='Choose from the following',reply_markup=reply_markup)


def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


# dispatcher.add_handler(InlineQueryHandler(reply_to_query))
# dispatcher.add_handler(ChosenInlineResultHandler(process_result, pass_job_queue=True))
dispatcher.add_handler(CommandHandler("join_game", join_game))
dispatcher.add_handler(CommandHandler("city", city))
dispatcher.add_handler(CommandHandler("start_game", start_game, pass_args=True, pass_job_queue=True))
updater.start_polling()
# updater.idle()
