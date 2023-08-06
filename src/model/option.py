from ..model.action import Action


class Option:
    def __init__(self, action: Action) -> None:
        self._action = action

    @property
    def action(self) -> Action:
        return self._action

    @property
    def name(self) -> str:
        return self._action.name
    
    def __str__(self) -> str:
        return self.name


CALL_BLUFF: Option = Option(action=Action.CALL_BLUFF)
DRAW: Option = Option(action=Action.DRAW)
PASS: Option = Option(action=Action.PASS)
