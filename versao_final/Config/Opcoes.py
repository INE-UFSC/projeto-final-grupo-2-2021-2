from Enums.Enums import Dificuldade
from Singleton.Singleton import Singleton


class Opcoes(Singleton):

    def __init__(self) -> None:
        if not super().created:
            self.__dificuldade = Dificuldade.medio
            self.__nome = 'Tatakae'
            self.__tocar_musica = True
            self.__menor_unidade = 24
            self.__tamanho_tela = (1128, 768)
            self.__GAME_TITLE = 'The Binding of Isaac'

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

    @property
    def TAMANHO_TELA(self) -> tuple:
        return self.__tamanho_tela

    @property
    def MENOR_UNIDADE(self) -> int:
        return self.__menor_unidade

    @property
    def GAME_TITLE(self) -> str:
        return self.__GAME_TITLE
