from Enums.Enums import Dificuldade
from Singleton.Singleton import Singleton


class Opcoes(Singleton):

    def __init__(self) -> None:
        if not super().created:
            self.__dificuldade = Dificuldade.medio
            self.__nome = 'Tatakae'
            self.__tocar_musica = True

    @property
    def tocar_musica(self) -> bool:
        return self.__tocar_musica

    @tocar_musica.setter
    def tocar_musica(self, value) -> None:
        if type(value) == bool:
            self.__tocar_musica = value

    @property
    def dificuldade(self) -> Dificuldade:
        return self.__dificuldade

    @dificuldade.setter
    def dificuldade(self, dificuldade) -> None:
        if isinstance(dificuldade, Dificuldade):
            self.__dificuldade = dificuldade

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, value) -> None:
        if type(value) == str:
            self.__nome = value
