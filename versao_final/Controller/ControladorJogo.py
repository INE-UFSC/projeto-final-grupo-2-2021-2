from Fases.Fase1 import Fase1
from Fases.Fase2 import Fase2
from Fases.Fase3 import Fase3
from Personagens.Jogador.Jogador import Jogador
from Views.Opcoes import Opcoes
from Abstractions.AbstractFase import AbstractFase


class ControladorJogo():
    def __init__(self, jogador: Jogador, opcoes: Opcoes) -> None:
        self.__fases = []
        self.__fases.append(Fase1(jogador, opcoes))
        self.__fases.append(Fase2(jogador, opcoes))
        self.__fases.append(Fase3(jogador, opcoes))

    def proxima_fase(self) -> AbstractFase:
        if len(self.__fases) > 0:
            self.__fases[0].load()
            return self.__fases.pop(0)
        else:
            return None
