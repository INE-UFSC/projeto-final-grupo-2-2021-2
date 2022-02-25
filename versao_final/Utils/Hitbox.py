class Hitbox():
    def __init__(self, posicao: tuple, tamanho: tuple) -> None:
        self.__posicao = posicao
        self.__tamanho = tamanho

    @property
    def center(self) -> tuple:
        x = self.__posicao[0] + self.__tamanho[0] // 2
        y = self.__posicao[1] + self.__tamanho[1] // 2
        return (x, y)

    @property
    def topright(self) -> tuple:
        x = self.__posicao[0] + self.__tamanho[0]
        y = self.__posicao[1]
        return (x, y)

    @property
    def topleft(self) -> tuple:
        return self.__posicao

    @property
    def bottomleft(self) -> tuple:
        x = self.__posicao[0]
        y = self.__posicao[1] + self.__tamanho[1]
        return (x, y)
    
    @property
    def bottomright(self) -> tuple:
        x = self.__posicao[0] + self.__tamanho[0]
        y = self.__posicao[1] + self.__tamanho[1]
        return (x, y)

    @property
    def posicao(self) -> tuple:
        return self.__posicao

    @property
    def tamanho(self) -> tuple:
        return self.__tamanho

    @posicao.setter
    def posicao(self, posicao: tuple) -> None:
        if type(posicao) == tuple and len(posicao) == 2:
            self.__posicao = posicao

    @property
    def x(self) -> int:
        return self.__posicao[0]

    @x.setter
    def x(self, x) -> None:
        if type(x) == int:
            nova_posicao = (x, self.__posicao[1])
            self.__posicao = nova_posicao

    @property
    def y(self) -> int:
        return self.__posicao[1]

    @y.setter
    def y(self, y) -> None:
        if type(y) == int:
            nova_posicao = (self.__posicao[0], y)
            self.__posicao = nova_posicao

    @property
    def altura(self) -> int:
        return self.__tamanho[0]

    @altura.setter
    def altura(self, altura) -> None:
        if type(altura) == int:
            novo_tamanho = (altura, self.__tamanho[1])
            self.__tamanho = novo_tamanho

    @property
    def largura(self) -> int:
        return self.__tamanho[1]

    @largura.setter
    def largura(self, largura) -> None:
        if type(largura) == int:
            novo_tamanho = (self.__tamanho[0], largura)
            self.__tamanho = novo_tamanho
