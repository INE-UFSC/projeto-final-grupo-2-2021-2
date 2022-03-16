from Views.States.AbstractState import AbstractState
from Views.Views.MenuView import MenuView
from Config.Enums import States


class QuitState(AbstractState):
    __STATE = States.QUIT

    def __init__(self) -> None:
        view = MenuView()
        super().__init__(view, QuitState.__STATE)
