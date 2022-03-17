from typing import List
from Jogo.ControllerJogo import ControllerJogo
from Screen.States.AbstractState import AbstractState
from Screen.Views.PlayingView import PlayingView
from Config.Enums import States
from Config.TelaJogo import TelaJogo
from pygame.event import Event
from Jogo.Jogo import Jogo
from Screen.Views.WinnerView import WinnerView


class WinnerState(AbstractState):
    __STATE = States.WINNER

    def __init__(self) -> None:
        view = PlayingView()
        self.__winner_view = WinnerView()
        self.__jogoOptions = ControllerJogo()
        self.__RUNNING = False
        super().__init__(view, WinnerState.__STATE)

    def run(self, events: List[Event]) -> States:
        if not self.__RUNNING:
            self.__RUNNING = True
            self.__jogo: Jogo = self.__jogoOptions.current_game()

        next_state = self.__winner_view.run(events)
        return next_state

    def desenhar(self, tela: TelaJogo) -> None:
        if not self.__RUNNING:
            self.__RUNNING = True
            self.__jogo: Jogo = self.__jogoOptions.current_game()

        self.view.desenhar(tela)
        self.__jogo.desenhar(tela)
        self.__winner_view.desenhar(tela)
