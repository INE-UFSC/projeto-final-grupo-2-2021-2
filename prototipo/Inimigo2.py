from abstractions.AbstractInimigo import AbstractInimigo
from stats import Inimigo2Stats


class Inimigo2(AbstractInimigo):
    def __init__(self, posicao: tuple) -> None:
        super().__init__(stats=Inimigo2Stats, posicao=posicao, tamanho=(6, 6))
        self.__sprite_path = ""

    @property
    def sprite_path(self) -> str:
        return self.__sprite_path
