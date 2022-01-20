from enum import Enum


class Dificuldade(Enum):
    facil = 1
    medio = 2
    dificil = 3


class Opcoes():
    def __init__(self, dificuldade=Dificuldade) -> None:
        if isinstance(dificuldade, Dificuldade):
            self.__dificuldade = dificuldade
        else:
            self.__dificuldade = Dificuldade.facil

    @property
    def dificuldade(self) -> Dificuldade:
        return self.__dificuldade

    @dificuldade.setter
    def dificuldade(self, dificuldade) -> None:
        if isinstance(dificuldade, Dificuldade):
            self.__dificuldade = dificuldade
