from abstractions.AbstractInimigo import AbstractInimigo
from stats import Inimigo3Stats


class Inimigo3(AbstractInimigo):
    def __init__(self, posicao: tuple) -> None:
        super().__init__(stats=Inimigo3Stats, posicao=posicao, tamanho=(3, 3))
        self.__sprite_path = ""

    @property
    def sprite_path(self) -> str:
        return self.__sprite_path
