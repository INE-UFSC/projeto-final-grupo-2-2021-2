from abc import ABC, abstractmethod
from Utils.Hitbox import Hitbox
from Personagens.Arma import Arma
import pygame


class AbstractPersonagem(ABC):
    def __init__(self, stats: dict, posicao: tuple, tamanho: tuple, terreno: None, sprite_paths: list) -> None:
        """Recebe um dicionário com os stats iniciais, tuplas com a posição e tamanho do personagem"""

        self.__vida_maxima = stats['vida'] if 'vida' in stats.keys() else 0
        self.__vida = self.__vida_maxima

        self.__ataque = stats['ataque'] if 'ataque' in stats.keys() else 0
        self.__defesa = stats['defesa'] if 'defesa' in stats.keys() else 0
        self.__vel = stats['vel'] if 'vel' in stats.keys() else 0

        self.__hitbox = Hitbox(posicao, tamanho)

        dano = stats['arma_dano'] if 'arma_dano' in stats.keys() else 0
        alcance = stats['arma_alcance'] if 'arma_alcance' in stats.keys() else 0

        self.__arma = Arma(dano, alcance)

        self.__terreno = terreno

        # O sprite path recebido deve ser uma lista com 4 valores, que será o caminho
        # para o sprite da 1º Esquerda, 2º Direita, 3º Cima, 4º Baixo
        self.__sprite_path = None
        if len(sprite_paths) == 4:
            self.__sprite_path = sprite_paths[3]  # Inicializa com o sprite para baixo
            self._sprite_esquerda = sprite_paths[0]
            self._sprite_direita = sprite_paths[1]
            self._sprite_cima = sprite_paths[2]
            self._sprite_baixo = sprite_paths[3]

        self.__direction = pygame.K_UP

    def tomar_dano(self, dano: int) -> int:
        if type(dano) == int:
            dano_real = dano - self.__defesa
            self.__vida -= dano_real

            return dano_real
        else:
            return 0

    def _atualizar_sprite(self, esquerda, direita, cima, baixo):
        if cima:
            self.sprite_path = self._sprite_cima
        elif direita:
            self.sprite_path = self._sprite_direita
        elif esquerda:
            self.sprite_path = self._sprite_esquerda
        elif baixo:
            self.sprite_path = self._sprite_baixo

    def update(self):
        self.__arma.update()

    def checar_atacando(self) -> bool:
        return self.__arma.desenhando_ataque

    @property
    def alcance(self) -> int:
        return self.__arma.alcance

    @property
    def vida_maxima(self) -> int:
        return self.__vida_maxima

    @vida_maxima.setter
    def vida_maxima(self, value: int) -> None:
        if type(value) == int and value > -1:
            self.__vida_maxima = value

    @property
    def vida(self) -> int:
        return self.__vida

    @vida.setter
    def vida(self, value: int) -> None:
        if type(value) == int:
            self.__vida = value

    @property
    def vel(self) -> int:
        return self.__vel

    @vel.setter
    def vel(self, value: int) -> None:
        if type(value) == int:
            self.__vel = value

    @property
    def hitbox(self) -> Hitbox:
        return self.__hitbox

    @property
    def arma(self) -> Arma:
        return self.__arma

    @arma.setter
    def arma(self, arma) -> None:
        if isinstance(arma, Arma):
            self.__arma = arma

    @property
    def dano(self) -> int:
        return self.__ataque + self.__arma.dano

    @property
    def terreno(self):
        return self.__terreno

    @terreno.setter
    def terreno(self, value) -> None:
        self.__terreno = value

    @property
    def sprite_path(self) -> str:
        return self.__sprite_path

    @sprite_path.setter
    def sprite_path(self, value) -> None:
        if type(value) == str:
            self.__sprite_path = value

    @abstractmethod
    def atacar(self):
        pass
