from typing import List
from DAO.JogoOptions import JogoOptions
from Screen.States.AbstractState import AbstractState
from Screen.Views.StaticView import StaticView
from pygame.event import Event
from Config.Enums import States


class CreateNewGameState(AbstractState):
    __STATE = States.CREATE_NEW

    def __init__(self) -> None:
        view = StaticView()
        self.__jogoOptions = JogoOptions()
        super().__init__(view, CreateNewGameState.__STATE)

    def run(self, events: List[Event]) -> States:
        self.__jogoOptions.create_new_game()
        print(self.__jogoOptions.current_game)
        return States.PLAYING
