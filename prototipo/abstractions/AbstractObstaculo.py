from abc import ABC
from Hitbox import Hitbox


class AbstractObstaculo(ABC):
    def __init__(self, posicao: tuple, tamanho: tuple, sprite_path: str) -> None:
        self.__hitbox = Hitbox(posicao=posicao, tamanho=tamanho)
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
