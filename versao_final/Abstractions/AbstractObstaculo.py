from abc import ABC
from Utils.Hitbox import Hitbox
from Config.Opcoes import Opcoes


class AbstractObstaculo(ABC):
    def __init__(self, posicao: tuple, sprite_path: str) -> None:
        config = Opcoes()
        MENOR_UNIDADE = config.MENOR_UNIDADE
        nova_position = (posicao[0]*MENOR_UNIDADE, posicao[1]*MENOR_UNIDADE)
        novo_tamanho = (MENOR_UNIDADE, MENOR_UNIDADE)

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
