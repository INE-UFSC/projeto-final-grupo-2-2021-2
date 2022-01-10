from AbstractPersonagem import AbstractPersonagem
from stats import Inimigo1Stats


class Inimigo1(AbstractPersonagem):
    def __init__(self, posicao: tuple, tamanho: tuple) -> None:
        super().__init__(stats=Inimigo1Stats, posicao=posicao, tamanho=tamanho)

    def mover(self):
        pass
