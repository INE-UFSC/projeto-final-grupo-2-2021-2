from abstractions.AbstractObstaculo import AbstractObstaculo


class Parede(AbstractObstaculo):
    def __init__(self, posicao: tuple, tamanho: tuple) -> None:
        super().__init__(posicao=posicao, tamanho=tamanho)
        self.__sprite_path = ""

    @property
    def sprite_path(self) -> str:
        return self.__sprite_path
