from AbstractPersonagem import AbstractPersonagem
from stats import Inimigo2Stats


class Inimigo2(AbstractPersonagem):
    def __init__(self, posicao: tuple, tamanho: tuple) -> None:
        super().__init__(stats=Inimigo2Stats, posicao=posicao, tamanho=tamanho)

    def mover(self):
        pass
