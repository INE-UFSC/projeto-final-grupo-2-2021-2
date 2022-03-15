from abc import abstractmethod
from typing_extensions import Self
from Config.TelaJogo import TelaJogo
from Views.Views.AbstractView import AbstractView
from Config.Enums import States


class AbstractState:
    def __init__(self, view: AbstractView, state: States) -> None:
        self.__view: AbstractView = view
        self.__state: States = state

    @property
    def view(self) -> AbstractView:
        return self.__view

    @property
    def state(self) -> States:
        return self.__state

    def run(self) -> States:
        next_state = self.__view.run()
        return next_state

    def desenhar(self, tela: TelaJogo) -> None:
        self.__view.desenhar(tela)
