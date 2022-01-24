from abc import ABC, abstractmethod

from pygame import sprite
from Hitbox import Hitbox
from Arma import Arma
from abstractions.AbstractTerreno import AbstractTerreno


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

        if isinstance(terreno, AbstractTerreno):
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

    @property
    def vida_maxima(self) -> int:
        """Retorna a vida máxima do personagem"""
        return self.__vida_maxima

    @vida_maxima.setter
    def vida_maxima(self, value: int) -> None:
        """Setter de vida_maxima"""
        if type(value) == int and value > -1:
            self.__vida_maxima = value

    @property
    def vida(self) -> int:
        """Retorna a vida atual do personagem"""
        return self.__vida

    @vida.setter
    def vida(self, value: int) -> None:
        """Setter de vida"""
        if type(value) == int:
            self.__vida = value

    @property
    def ataque(self) -> int:
        """Retorna o valor de ataque do personagem"""
        return self.__ataque

    @ataque.setter
    def ataque(self, value: int) -> None:
        """Setter de ataque"""
        if type(value) == int:
            self.__ataque = value

    @property
    def defesa(self) -> int:
        """Retorna o valor de defesa do personagem"""
        return self.__defesa

    @defesa.setter
    def defesa(self, value: int) -> None:
        """Setter de defesa"""
        if type(value) == int:
            self.__defesa = value

    @property
    def vel(self) -> int:
        """Retorna a velocidade do personagem"""
        return self.__vel

    @vel.setter
    def vel(self, value: int) -> None:
        """Setter de velocidade"""
        if type(value) == int:
            self.__vel = value

    @property
    def hitbox(self) -> Hitbox:
        return self.__hitbox

    @property
    def arma(self) -> Arma:
        """Retorna a arma que esse personagem possui"""
        return self.__arma

    @arma.setter
    def arma(self, arma) -> None:
        if isinstance(arma, Arma):
            self.__arma = arma

    def tomar_dano(self, dano: int) -> int:
        """Retorna o quanto de vida foi retirado do personagem"""
        if type(dano) == int:
            dano_real = dano - self.__defesa
            self.__vida -= dano_real

            return dano_real
        else:
            return 0

    @property
    def dano(self) -> int:
        """Retorna o dano causado por um ataque do personagem"""
        return self.__ataque + self.__arma.dano

    @abstractmethod
    def atacar(self):
        pass

    @property
    def terreno(self) -> AbstractTerreno:
        return self.__terreno

    @terreno.setter
    def terreno(self, value) -> None:
        if isinstance(value, AbstractTerreno):
            self.__terreno = value

    @property
    def sprite_path(self) -> str:
        return self.__sprite_path

    @sprite_path.setter
    def sprite_path(self, value) -> None:
        if type(value) == str:
            self.__sprite_path = value

    def _atualizar_frente(self, esquerda, direita, cima, baixo):
        """Atualiza o sprite path conforme o personagem anda"""
        if cima:
            self.sprite_path = self._sprite_cima
        elif direita:
            self.sprite_path = self._sprite_direita
        elif esquerda:
            self.sprite_path = self._sprite_esquerda
        elif baixo:
            self.sprite_path = self._sprite_baixo
