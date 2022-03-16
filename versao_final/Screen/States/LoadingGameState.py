from typing import List
from DAO.JogoOptions import JogoOptions
from Screen.States.AbstractState import AbstractState
from Screen.Views.StaticView import StaticView
from pygame.event import Event
from Config.Enums import States


class LoadingGameState(AbstractState):
    __STATE = States.LOAD_GAME

    def __init__(self) -> None:
        view = StaticView()
        self.__jogoOptions = JogoOptions()
        super().__init__(view, LoadingGameState.__STATE)

    def run(self, events: List[Event]) -> States:
        self.__jogoOptions.load_game()
        print('Retornando Playing')
        return States.PLAYING
