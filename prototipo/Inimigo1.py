from abstractions.AbstractInimigo import AbstractInimigo
from stats import Inimigo1Stats


class Inimigo1(AbstractInimigo):
    def __init__(self, posicao: tuple) -> None:
        super().__init__(stats=Inimigo1Stats, posicao=posicao, tamanho=(5, 5))
        self.__sprite_path = ""

    @property
    def sprite_path(self) -> str:
        return self.__sprite_path
