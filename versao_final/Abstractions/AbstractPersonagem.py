from abc import ABC, abstractmethod
import pygame
from Utils.Hitbox import Hitbox
from Personagens.Arma import Arma


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

    @property
    def posicao_frente(self):
        posicao = self.__hitbox.posicao
        tamanho = self.__hitbox.tamanho

        rect = pygame.Rect(posicao, tamanho)
        if self.__direction == pygame.K_UP:
            return rect.midtop
        elif self.__direction == pygame.K_LEFT:
            return rect.midleft
        elif self.__direction == pygame.K_RIGHT:
            return rect.midright
        else:
            return rect.midbottom

    def get_rect_arma(self) -> pygame.Rect:
        posicao_frente = self.posicao_frente

        rect = pygame.Rect(posicao_frente, (self.arma.alcance, self.arma.alcance))
        rect.center = posicao_frente
        return rect

    @property
    def alcance(self) -> int:
        return self.__arma.alcance

    def checar_atacando(self) -> bool:
        return self.__arma.desenhando_ataque

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
    def ataque(self) -> int:
        return self.__ataque

    @ataque.setter
    def ataque(self, value: int) -> None:
        if type(value) == int:
            self.__ataque = value

    @property
    def defesa(self) -> int:
        return self.__defesa

    @defesa.setter
    def defesa(self, value: int) -> None:
        if type(value) == int:
            self.__defesa = value

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

    @abstractmethod
    def atacar(self):
        pass

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

    def tomar_dano(self, dano: int) -> int:
        """Retorna o quanto de vida foi retirado do personagem"""
        if type(dano) == int:
            dano_real = dano - self.__defesa
            self.__vida -= dano_real

            return dano_real
        else:
            return 0

    def _atualizar_sprite(self, esquerda, direita, cima, baixo):
        """Atualiza o sprite path conforme o personagem anda"""
        if cima:
            self.sprite_path = self._sprite_cima
            self.__direction = pygame.K_UP
        elif direita:
            self.sprite_path = self._sprite_direita
            self.__direction = pygame.K_RIGHT
        elif esquerda:
            self.sprite_path = self._sprite_esquerda
            self.__direction = pygame.K_LEFT
        elif baixo:
            self.sprite_path = self._sprite_baixo
            self.__direction = pygame.K_DOWN

    def update(self):
        self.__arma.update()
