from abc import ABC, abstractmethod
from Hitbox import Hitbox
from Arma import Arma


class AbstractPersonagem(ABC):
    def __init__(self, stats: dict, posicao: tuple, tamanho: tuple) -> None:
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