class AlreadyCreated(Exception):
    def __str__(self):
        return "Game already created!"


class AlreadyJoined(Exception):
    def __str__(self):
        return "Already in game!"


class AlreadyRunning(Exception):
    def __str__(self):
        return "Game already started!"


class GameNotCreated(Exception):
    def __str__(self):
        return "Game is not created!"


class GameNotReady(Exception):
    def __str__(self):
        return "More players are needed to play!"


class NotInGame(Exception):
    def __str__(self):
        return "You are not playing!"
