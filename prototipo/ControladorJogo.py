from Fase1 import Fase1
from Jogador import Jogador
from Opcoes import Opcoes
from abstractions.AbstractFase import AbstractFase


class ControladorJogo():
    def __init__(self, jogador: Jogador, tamanho_tela: tuple, opcoes: Opcoes) -> None:
        self.__fases = []
        self.__fases.append(Fase1(jogador, tamanho_tela, opcoes))

    def proxima_fase(self) -> AbstractFase:
        if len(self.__fases) > 0:
            self.__fases[0].load()
            return self.__fases.pop(0)
        else:
            return None
