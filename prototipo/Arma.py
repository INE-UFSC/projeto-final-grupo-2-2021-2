class Arma():
    def __init__(self, dano, alcance) -> None:
        self.__dano = dano
        self.__alcance = alcance
        self.__atacando = False

    @property
    def dano(self) -> int:
        """Retorna o dano da arma"""
        return self.__dano

    @property
    def alcance(self) -> int:
        """Retorna o alcance de ataque da arma"""
        return self.__alcance
