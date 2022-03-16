from abc import abstractmethod
from multiprocessing import Event
from typing import List
from Config.Opcoes import Opcoes
from Config.Enums import States
from pygame import Rect, Surface, event
from Config.TelaJogo import TelaJogo


class AbstractView:
    def __init__(self, state: States) -> None:
        self.__state: States = state
        self.__opcoes = Opcoes()
        self.__views_size = self.__opcoes.TAMANHO_TELA
        self.__position = self.__opcoes.POSICAO_TELAS

    @abstractmethod
    def desenhar(self, tela: TelaJogo) -> None:
        tela.janela.blit(self.image, self.rect)

    @abstractmethod
    def run(self, events: List[event.Event]) -> States:
        pass

    @property
    @abstractmethod
    def image(self) -> Surface:
        pass

    @property
    @abstractmethod
    def rect(self) -> Rect:
        pass

    @property
    def state(self) -> States:
        return self.__state

    @property
    def _views_size(self) -> tuple:
        return self.__views_size

    @property
    def _position(self) -> tuple:
        return self.__position
