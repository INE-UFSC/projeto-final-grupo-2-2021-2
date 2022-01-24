from abstractions.AbstractObstaculo import AbstractObstaculo


class Parede(AbstractObstaculo):
    def __init__(self, posicao: tuple, tamanho: tuple) -> None:
        sprite_path = ""

        super().__init__(posicao=posicao, tamanho=tamanho, sprite_path=sprite_path)
