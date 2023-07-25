from typing import Optional
from uuid import uuid4

from discord import Embed, Intents, Interaction, InteractionResponded, Message
from discord.ext.commands import Bot
from discord.ext.commands.context import Context
from discord.ui import Button, View

from src.model.Card import Card
from src.model.Color import Color, COLORS
from src.model.exceptions import *
from src.model.Player import Player
from src.model.Table import Table
from src.utils.token import DISCORD

intents = Intents.all()
bot = Bot(command_prefix="!", intents=intents)
table: Optional[Table] = None
message_id = 0


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        print(guild.name, guild.id)
        for member in guild.members:
            print(member.name)


@bot.tree.command(name="create")
async def create_game(interaction: Interaction) -> None:
    print(f"create interaction id {interaction.id}")
    global table
    table = Table()
    message: str = f"New game created! \n" \
                   f"Type /join to play!"
    await send_message_to_all(interaction=interaction, message=message)
    return None


@bot.tree.command(name="join")
async def join_game(interaction: Interaction) -> None:
    print(f"join interaction id {interaction.id}")
    player_name: str = interaction.user.name
    player_id: int = interaction.user.id
    new_player: Player = Player(name=player_name, id_=player_id)
    try:
        table.add_player(player=new_player)
        message: str = f"Joined the game!"
    except AlreadyJoined as e:
        message = f"{e}"

    await send_message_to_all(interaction=interaction, message=message)
    return None


@bot.tree.command(name="leave")
async def leave_game(interaction: Interaction) -> None:
    player_id: int = interaction.user.id
    player: Player = table.get_player(player_id=player_id)
    try:
        table.remove_player(player=player)
        message: str = f"Left the game!"
    except NotInGame as e:
        message = f"{e}"

    await send_message_to_all(interaction=interaction, message=message)
    return None


@bot.tree.command(name="start")
async def start_game(interaction: Interaction) -> None:
    print(f"start interaction id {interaction.id}")
    try:
        table.start_game()
    except (AttributeError, AlreadyRunning, GameNotReady) as e:
        message = f"{e}"
        await send_message_to_all(interaction=interaction, message=message)
    else:
        await send_message_to_all(interaction=interaction, message="Game started!")
        await status(interaction=interaction)

    return None


def make_choice() -> View:
    view: View = View(timeout=None)
    button = Button(label="Make your choice!")
    button.callback = show_cards
    view.add_item(button)
    return view


async def show_cards(interaction: Interaction) -> None:
    view: View = _show_cards(interaction=interaction)
    await interaction.response.send_message("oi", view=view, ephemeral=True)
    return None


def _show_cards(interaction: Interaction) -> View:
    print(f"show_cards interaction id {interaction.id}")
    view: View = View(timeout=None)
    current_player: Player = table.current_player()
    user_id: int = interaction.user.id
    player: Player = table.get_player(user_id)
    # if (player is None):
    #     return None

    if (table.choosing_color()) and (user_id == current_player.id()):
        view = choose_color()
    elif (user_id == current_player.id()):
        playable_cards = table.playable_cards
        if (current_player.not_have_playable_card(playable_cards=playable_cards)):
            sticker_id = "option_draw"
            new_button: Button = Button(label="draw", custom_id=sticker_id)
            new_button.callback = selected_card
            view.add_item(new_button)
            if (current_player.num_cards() < 25):
                _disable_all_cards(view=view, player=current_player)
        else:
            _gen_sticker_cards(view=view, player=current_player,
                               playable_cards=playable_cards)
    else:
        _disable_all_cards(view=view, player=player)

    return view


def _gen_sticker_cards(view: View, player: Player,
                       playable_cards: set[Card]) -> None:
    added_cards: list[str] = []
    for card in player.get_cards():
        card_name: str = str(card).lower()
        if (card_name in added_cards) or (card not in playable_cards):
            if (player.num_cards() > 25):
                continue
            sticker_id: str = str(uuid4())
            disabled: bool = True
        else:
            sticker_id = card_name
            added_cards.append(card_name)
            disabled = False

        new_button: Button = Button(label=card_name, custom_id=sticker_id, disabled=disabled)
        new_button.callback = selected_card
        view.add_item(new_button)
    return None


def _disable_all_cards(view: View, player: Player) -> None:
    for card in player.get_cards():
        card_name: str = str(card).lower()
        sticker_id: str = str(uuid4())
        new_sticker: Button = Button(label=card_name, custom_id=sticker_id, disabled=True)
        view.add_item(new_sticker)

    return None


async def selected_card(interaction: Interaction) -> None:
    print(f"selected card interaction id {interaction.id}")
    current_player: Player = table.current_player()
    sender_id = interaction.user.id
    card_name: str = interaction.data["custom_id"]
    try:
        card_name: Color = Color[card_name]
    except KeyError:
        pass

    if (current_player.id() == sender_id):
        if isinstance(card_name, Color):
            selected: Color = card_name
            # await send_message_to_all(interaction=interaction, message=str(selected))
        else:
            selected: Card = current_player.select_card(name=card_name)
        table.turn(selected=selected)
        if (table.terminated()):
            await send_message_to_all(interaction=interaction,
                                      message=f"Game ended, {table.current_player()} won!")
        else:
            await edit(interaction=interaction)
        try:
            await interaction.response.defer()
        except InteractionResponded:
            pass

    return None


async def status(interaction: Interaction) -> None:
    print(f"status interaction id {interaction.id}")
    card_name: str = str(table.current_card()).lower() + ".png"
    embed = Embed(description=table.status(), title=f"{table.current_player()} Turn")
    embed.set_thumbnail(
        url=f"https://raw.githubusercontent.com/G-Carneiro/UNO/main/Cards/{card_name}")
    global message_id
    message: Message = await interaction.channel.send(view=make_choice(), embed=embed)
    message_id = message.id
    return None


async def edit(interaction: Interaction) -> None:
    print(f"edit interaction id {interaction.id}")
    card_name: str = str(table.current_card()).lower() + ".png"
    channel = interaction.channel
    message: Message = await channel.fetch_message(message_id)
    embed = Embed(description=table.status(), title=f"{table.current_player()} Turn")
    embed.set_thumbnail(
        url=f"https://raw.githubusercontent.com/G-Carneiro/UNO/main/Cards/{card_name}")
    await message.edit(embed=embed)
    view: View = _show_cards(interaction=interaction)
    await interaction.edit_original_response(view=view)
    # await interaction.response.edit_message()
    # print(teste, teste.embeds)


def choose_color() -> View:
    view: View = View(timeout=None)
    for color in COLORS:
        message: str = str(color)
        num_cards: int = table.current_player().num_color_card(color)
        button: Button = Button(label=f"{message} ({num_cards})", custom_id=color.name)
        button.callback = selected_card
        view.add_item(button)

    return view


@bot.tree.command(name="skip")
async def skip(interaction: Interaction) -> None:
    if (table.running()):
        table.skip()

    await edit(interaction=interaction)
    return None


async def send_message_to_all(interaction: Interaction, message: str) -> None:
    await interaction.response.send_message(message)
    return None


@bot.command()
async def sync(ctx: Context):
    await bot.tree.sync()
    await ctx.send("Done: slash commands")


bot.run(DISCORD)
