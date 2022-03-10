from abc import ABC, abstractmethod
from Config.Enums import Dificuldade
from Config.Opcoes import Opcoes
from Personagens.Jogador import Jogador
from Config.TelaJogo import TelaJogo
from Terrenos.AbstractTerreno import AbstractTerreno


class AbstractFase(ABC):
    def __init__(self, jogador: Jogador) -> None:
        self.__jogador: Jogador = jogador
        self.__terreno: AbstractTerreno = None
        self.__opcoes = Opcoes()
        self.__dificuldade = self.__opcoes.dificuldade
        self.__jogador = jogador

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

    def desenhar(self, tela: TelaJogo) -> None:
        self.__terreno.desenhar(tela)

    def run(self) -> None:
        """Função para ser executada em todo ciclo do main loop"""
        self.__terreno.animate()
        self.__jogador.processar_inputs()
        self.__terreno.mover_inimigos()
        self.__terreno.lidar_ataques()
        self.__terreno.update()

    @property
    def _dificuldade(self) -> Dificuldade:
        return self.__dificuldade

    @property
    def _jogador(self) -> Jogador:
        return self.__jogador

    @property
    def _terreno(self) -> AbstractTerreno:
        return self.__terreno

    def _set_terreno(self, terreno: AbstractTerreno) -> None:
        if isinstance(terreno, AbstractTerreno):
            self.__terreno = terreno

    @abstractmethod
    def load(self) -> None:
        pass
