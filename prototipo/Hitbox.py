class Hitbox():
    def __init__(self, position: tuple, tamanho: tuple) -> None:
        self.__position = position
        self.__tamanho = tamanho

    @property
    def position(self) -> tuple:
        return self.__position

    @property
    def tamanho(self) -> tuple:
        return self.__tamanho
