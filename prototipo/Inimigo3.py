from AbstractPersonagem import AbstractPersonagem
from stats import Inimigo3Stats


class Inimigo3(AbstractPersonagem):
    def __init__(self, posicao: tuple, tamanho: tuple) -> None:
        super().__init__(stats=Inimigo3Stats, posicao=posicao, tamanho=tamanho)

    def mover(self):
        pass
