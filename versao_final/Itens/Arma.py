class Arma:
    def __init__(self, dano, alcance) -> None:
        self.__dano = dano
        self.__alcance = alcance

    @property
    def dano(self) -> int:
        return self.__dano

    @property
    def alcance(self) -> int:
        return self.__alcance
