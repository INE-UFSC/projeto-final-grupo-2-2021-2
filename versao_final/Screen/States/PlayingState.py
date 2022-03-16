from typing import List
from pygame import K_ESCAPE, KEYDOWN
from DAO.JogoDAO import JogoDAO
from DAO.JogoOptions import JogoOptions
from Screen.States.AbstractState import AbstractState
from Screen.Views.PauseView import PauseView
from Screen.Views.PlayingView import PlayingView
from Config.Enums import States
from Config.TelaJogo import TelaJogo
from pygame.event import Event
from Controllers.Jogo import Jogo


class PlayingState(AbstractState):
    __STATE = States.PLAYING
    __RUNNING = False

    def __init__(self) -> None:
        view = PlayingView()
        self.__dao = JogoDAO()
        self.__jogoOptions = JogoOptions()
        self.__pause_screen = PauseView()
        self.__paused = False
        self.__timer = 2000
        super().__init__(view, PlayingState.__STATE)

    def run(self, events: List[Event]) -> States:
        if not PlayingState.__RUNNING:
            PlayingState.__RUNNING = True
            self.__jogo: Jogo = self.__jogoOptions.current_game()

        if self.__timer > 0:
            self.__timer -= 1
        if self.__timer == 5:
            print('Iniciando')
            for inimigo in self.__jogo.controlador.current_fase.current_map.inimigos:
                print(inimigo.hitbox.posicao)
            self.__dao.add(self.__jogo)

        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.__paused = not self.__paused

        if self.__paused:
            next_state = self.__pause_screen.run(events)
            return next_state
        else:
            self.__jogo.run(events)

        if self.__jogo.player_has_lost():
            return States.MENU
        return States.SAME

    def desenhar(self, tela: TelaJogo) -> None:
        if not PlayingState.__RUNNING:
            self.__jogo: Jogo = self.__jogoOptions.current_game()
            print('Desenhar')
            print(self.__jogo.controlador.current_fase.current_map.inimigos)
            PlayingState.__RUNNING = True

        self.view.desenhar(tela)
        self.__jogo.desenhar(tela)
        if self.__paused:
            self.__pause_screen.desenhar(tela)
