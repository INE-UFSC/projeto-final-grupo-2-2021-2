class Hitbox():
    def __init__(self, posicao: tuple, tamanho: tuple) -> None:
        self.__posicao = posicao
        self.__tamanho = tamanho

    @property
    def posicao(self) -> tuple:
        return self.__posicao

    @property
    def tamanho(self) -> tuple:
        return self.__tamanho
