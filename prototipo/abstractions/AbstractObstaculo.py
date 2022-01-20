from abc import ABC, abstractmethod
from Hitbox import Hitbox


class AbstractObstaculo(ABC):
    def __init__(self, posicao=tuple, tamanho=tuple) -> None:
        self.__hitbox = Hitbox(posicao=posicao, tamanho=tamanho)

    @property
    def hitbox(self) -> Hitbox:
        return self.__hitbox

    @property
    @abstractmethod
    def sprite_path(self) -> str:
        pass
