from abstractions.AbstractObstaculo import AbstractObstaculo


class Buraco(AbstractObstaculo):
    def __init__(self, posicao: tuple) -> None:
        sprite_path = ""

        super().__init__(posicao=posicao, sprite_path=sprite_path)
