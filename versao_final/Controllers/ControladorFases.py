from Fases.DungeonFase import DungeonFase
from Personagens.Jogador import Jogador
from Fases.AbstractFase import AbstractFase


class ControladorFases():
    def __init__(self, jogador: Jogador) -> None:
        self.__fases = []
        self.__fases.append(DungeonFase(jogador))

    def proxima_fase(self) -> AbstractFase:
        if len(self.__fases) > 0:
            self.__fases[0].load()
            return self.__fases.pop(0)
        else:
            return None
