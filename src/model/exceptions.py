class AlreadyCreated(Exception):
    """Game already created!"""


class AlreadyJoined(Exception):
    """Already in game!"""


class AlreadyRunning(Exception):
    """Game already started!"""


class GameNotCreated(Exception):
    """Game is not created!"""


class NeedMorePlayers(Exception):
    """More players are needed to play!"""


class NotInGame(Exception):
    """You are not playing!"""
