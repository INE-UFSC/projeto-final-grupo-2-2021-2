from abc import ABC, abstractmethod
from Utils.Hitbox import Hitbox
from Personagens.Arma import Arma
from Personagens.Status import Status


class AbstractPersonagem(ABC):
    def __init__(self, stats: dict, posicao: tuple, tamanho: tuple, terreno: None, sprite_paths: list) -> None:
        """Recebe um dicionário com os stats iniciais, tuplas com a posição e tamanho do personagem"""
        self.__status = Status(stats)

        dano = stats['arma_dano'] if 'arma_dano' in stats.keys() else 0
        alcance = stats['arma_alcance'] if 'arma_alcance' in stats.keys() else 0
        self.__arma = Arma(dano, alcance)

        self.__hitbox = Hitbox(posicao, tamanho)
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

    def tomar_dano(self, dano: int) -> int:
        if type(dano) == int:
            dano_real = dano - self.__status.defesa
            self.__status.vida -= dano_real

            return dano_real
        else:
            return 0

    def _atualizar_sprite(self, x_movement, y_movement):
        if y_movement < 0:
            self.sprite_path = self._sprite_cima
        elif x_movement > 0:
            self.sprite_path = self._sprite_direita
        elif x_movement < 0:
            self.sprite_path = self._sprite_esquerda
        elif y_movement > 0:
            self.sprite_path = self._sprite_baixo

    def update(self):
        self.__arma.update()

    def checar_atacando(self) -> bool:
        return self.__arma.desenhando_ataque

    @property
    def alcance(self) -> int:
        return self.__arma.alcance + self.__status.alcance

    @property
    def vida_maxima(self) -> int:
        return self.__status.vida_maxima

    @vida_maxima.setter
    def vida_maxima(self, value: int) -> None:
        self.__status.vida_maxima = value

    @property
    def vida(self) -> int:
        return self.__status.vida

    @vida.setter
    def vida(self, value: int) -> None:
        self.__status.vida = value

    @property
    def vel(self) -> int:
        return self.__status.vel

    @vel.setter
    def vel(self, value: int) -> None:
        self.__status.vel = value

    @property
    def dano(self) -> int:
        return self.__status.ataque + self.__arma.dano

    @property
    def invencibilidade(self) -> bool:
        return self.__status.invencibilidade

    @invencibilidade.setter
    def invencibilidade(self, value: bool) -> None:
        self.__status.invencibilidade = value

    @property
    def arma(self) -> Arma:
        return self.__arma

    @arma.setter
    def arma(self, arma) -> None:
        if isinstance(arma, Arma):
            self.__arma = arma

    @property
    def terreno(self):
        return self.__terreno

    @terreno.setter
    def terreno(self, value) -> None:
        self.__terreno = value

    @property
    def hitbox(self) -> Hitbox:
        return self.__hitbox

    @property
    def sprite_path(self) -> str:
        return self.__sprite_path

    @sprite_path.setter
    def sprite_path(self, value) -> None:
        if type(value) == str:
            self.__sprite_path = value
    
    @property
    def status(self):
        return self.__status

    @abstractmethod
    def atacar(self):
        pass
