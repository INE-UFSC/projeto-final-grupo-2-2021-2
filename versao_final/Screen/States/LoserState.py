from typing import List
from Jogo.ControllerJogo import ControllerJogo
from Screen.States.AbstractState import AbstractState
from Screen.Views.LoserView import LoserView
from Screen.Views.PlayingView import PlayingView
from Config.Enums import States
from Config.TelaJogo import TelaJogo
from pygame.event import Event
from Jogo.Jogo import Jogo


class LoserState(AbstractState):
    __STATE = States.LOSER

    def __init__(self) -> None:
        view = PlayingView()
        self.__loser_view = LoserView()
        self.__jogoOptions = ControllerJogo()
        self.__RUNNING = False
        super().__init__(view, LoserState.__STATE)

    def run(self, events: List[Event]) -> States:
        if not self.__RUNNING:
            self.__RUNNING = True
            self.__jogo: Jogo = self.__jogoOptions.current_game()

        next_state = self.__loser_view.run(events)
        return next_state

    def desenhar(self, tela: TelaJogo) -> None:
        if not self.__RUNNING:
            self.__RUNNING = True
            self.__jogo: Jogo = self.__jogoOptions.current_game()

        self.view.desenhar(tela)
        self.__jogo.desenhar(tela)
        self.__loser_view.desenhar(tela)
