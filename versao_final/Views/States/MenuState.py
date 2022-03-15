from tkinter.tix import Select
from Config.TelaJogo import TelaJogo
from Views.States.AbstractState import AbstractState
from Views.Views.MenuView import MenuView
from Config.Enums import States


class MenuState(AbstractState):
    __STATE = States.MENU

    def __init__(self) -> None:
        view = MenuView()
        super().__init__(view, MenuState.__STATE)
