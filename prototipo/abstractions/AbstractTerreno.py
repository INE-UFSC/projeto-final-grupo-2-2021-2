from abc import ABC, abstractmethod
from Hitbox import Hitbox


class AbstractTerreno(ABC):
    def __init__(self, inimigos: list, itens, tamanho_tela: tuple, obstaculos: list, jogador, sprite_path: str):
        self.__inimigos = inimigos
        self.__obstaculos = obstaculos
        self.__itens = itens
        self.__hitbox = Hitbox(posicao=(0, 0), tamanho=tamanho_tela)
        self.__jogador = jogador
        self.__sprite_path = sprite_path

    @property
    def sprite_path(self) -> str:
        return self.__sprite_path

    @sprite_path.setter
    def sprite_path(self, value) -> None:
        if type(value) == str:
            self.__sprite_path = value

    @property
    def jogador(self):
        """Retorna a instância do Jogador que está no Terreno"""
        return self.__jogador

    @property
    def hitbox(self) -> Hitbox:
        return self.__hitbox

    @property
    def itens(self):
        return self.__itens

    @property
    def inimigos(self) -> list:
        return self.__inimigos

    @property
    def obstaculos(self) -> list:
        return self.__obstaculos

    def load_inimigos(self, inimigos: list) -> None:
        self.__inimigos.append(inimigos)

    @abstractmethod
    def dropar_item():
        pass

    @abstractmethod
    def remover_inimigo():
        pass

    @abstractmethod
    def validar_movimento():
        pass

    @abstractmethod
    def iniciar_rodada():
        pass

    @abstractmethod
    def load_inimigos():
        pass

    @abstractmethod
    def has_ended():
        pass
