from abc import ABC, abstractmethod
from Hitbox import Hitbox


class AbstractTerreno(ABC):
    def __init__(self, inimigos: list, itens, tamanho_tela: tuple, obstaculos: list):
        self.__inimigos = inimigos
        self.__obstaculos = obstaculos
        self.__itens = itens
        self.__hitbox = Hitbox(posicao=(0, 0), tamanho=tamanho_tela)

    @property
    def hitbox(self) -> Hitbox:
        return self.__hitbox

    @property
    def item(self):
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
