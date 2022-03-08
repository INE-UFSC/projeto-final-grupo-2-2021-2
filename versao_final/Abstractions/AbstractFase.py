from abc import ABC, abstractmethod
from Enums.Enums import Dificuldade
from Personagens.Jogador.Jogador import Jogador
from Config.TelaJogo import TelaJogo
from Config.Opcoes import Opcoes
from Abstractions.AbstractTerreno import AbstractTerreno


class AbstractFase(ABC):
    def __init__(self, jogador: Jogador) -> None:
        self.__jogador: Jogador = jogador
        self.__opcoes = Opcoes()
        self.__dificuldade = self.__opcoes.dificuldade
        self.__terreno = None

    def player_has_lost(self) -> bool:
        if self.__jogador.morreu:
            return True
        else:
            return False

    def start(self, tela: TelaJogo):
        self.__jogador.terreno = self.__terreno
        self.__terreno.iniciar_rodada(tela)

    def has_ended(self) -> bool:
        return self.__terreno.has_ended()

    def ciclo(self, tela: TelaJogo) -> None:
        """Função para ser executada em todo ciclo do main loop"""
        self.__jogador.processar_inputs()
        self.__terreno.mover_inimigos()
        self.__terreno.lidar_ataques()
        self.__terreno.update()
        self.__terreno.desenhar(tela)

    @property
    def jogador(self) -> Jogador:
        return self.__jogador

    @property
    def terreno(self) -> AbstractTerreno:
        return self.__terreno

    @terreno.setter
    def terreno(self, value) -> None:
        if isinstance(value, AbstractTerreno):
            self.__terreno = value

    @property
    def dificuldade(self) -> Dificuldade:
        return self.__dificuldade

    @abstractmethod
    def load(self) -> None:
        pass
