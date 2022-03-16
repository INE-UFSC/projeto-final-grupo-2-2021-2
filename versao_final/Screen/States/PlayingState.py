from typing import List

from pygame import K_ESCAPE, KEYDOWN
import pygame
from Screen.States.AbstractState import AbstractState
from Screen.Views.PlayingView import PlayingView
from Config.Enums import States
from Config.TelaJogo import TelaJogo
from pygame.event import Event
from Controllers.Jogo import Jogo


class PlayingState(AbstractState):
    __STATE = States.PLAYING

    def __init__(self) -> None:
        view = PlayingView()
        self.__jogo = Jogo()
        # self.__pause_screen = TelaPause()
        self.__paused = False
        super().__init__(view, PlayingState.__STATE)

    def run(self, events: List[Event]) -> States:
        for event in events:
            if event.type == KEYDOWN:
                if event.key == pygame[K_ESCAPE]:
                    self.__paused = not self.__paused

        if self.__paused:
            # self.__pause_screen.run()
            pass
        self.__jogo.run(events)

        if self.__jogo.player_has_lost():
            return States.MENU
        return States.SAME

    def desenhar(self, tela: TelaJogo) -> None:
        self.view.desenhar(tela)
        self.__jogo.desenhar(tela)
        if self.__paused:
            pass
            # self.__pause_screen.desenhar(tela)
