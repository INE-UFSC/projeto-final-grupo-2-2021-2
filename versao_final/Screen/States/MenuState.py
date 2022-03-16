from Screen.States.AbstractState import AbstractState
from Screen.Views.MenuView import MenuView
from Config.Enums import States


class MenuState(AbstractState):
    __STATE = States.MENU

    def __init__(self) -> None:
        view = MenuView()
        super().__init__(view, MenuState.__STATE)
