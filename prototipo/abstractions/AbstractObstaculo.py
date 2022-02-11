from abc import ABC
from Hitbox import Hitbox

menor_unidade = 32


class AbstractObstaculo(ABC):
    def __init__(self, posicao: tuple, sprite_path: str) -> None:
        nova_position = (posicao[0]*menor_unidade, posicao[1]*menor_unidade)
        novo_tamanho = (menor_unidade, menor_unidade)

        self.__hitbox = Hitbox(posicao=nova_position, tamanho=novo_tamanho)
        self.__sprite_path = sprite_path

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
