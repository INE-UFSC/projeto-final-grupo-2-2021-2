from abc import ABC, abstractmethod
from Enums.Enums import Dificuldade
from Personagens.Jogador.Jogador import Jogador
from Config.TelaJogo import TelaJogo
from Config.Opcoes import Opcoes
from Abstractions.AbstractTerreno import AbstractTerreno


class AbstractFase(ABC):
    def __init__(self, jogador) -> None:
        self.__jogador = jogador
        self.__opcoes = Opcoes()
        self.__dificuldade = self.__opcoes.dificuldade
        self.__terreno = None

    def is_player_dead(self) -> bool:
        if self.__jogador.vida <= 0:
            return True
        else:
            return False

    def start(self, tela: TelaJogo):
        self.jogador.terreno = self.__terreno
        self.__terreno.iniciar_rodada(tela, self.jogador)

    def has_ended(self) -> bool:
        return self.__terreno.has_ended()

    def ciclo(self, tela: TelaJogo) -> None:
        """Função para ser executada em todo ciclo do main loop"""
        self.__jogador.lidar_inputs()
        if self.__jogador.verificar_ataque():
            self.__terreno.executar_ataque(tela, self.__jogador)

        for inimigo in self.__terreno.inimigos:
            inimigo.mover(self.__jogador.hitbox)
            if inimigo.verificar_ataque(self.__jogador.hitbox):
                if inimigo.atacar():
                    self.__terreno.executar_ataque_inimigo(tela, inimigo)

            inimigo.update(self.__jogador.hitbox)

        self.__jogador.update()
        self.__terreno.desenhar(tela, self.__jogador)
        self.__terreno.dropar_item()

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
