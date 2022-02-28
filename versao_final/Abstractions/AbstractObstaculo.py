from abc import ABC, abstractmethod

from pygame import Rect, Surface
from Utils.Hitbox import Hitbox


class AbstractObstaculo(ABC):
    def __init__(self, posicao: tuple, tamanho: tuple, transpassavel: bool) -> None:
        self.__transpassavel = transpassavel
        self.__hitbox = Hitbox(posicao=posicao, tamanho=tamanho)

    @property
    def transpassavel(self) -> bool:
        return self.__transpassavel

    @transpassavel.setter
    def transpassavel(self, value):
        if type(value) == bool:
            self.__transpassavel = value

    @property
    def hitbox(self) -> Hitbox:
        return self.__hitbox

    @property
    @abstractmethod
    def image(self) -> Surface:
        pass
    
    @property
    @abstractmethod
    def rect(self) -> Rect:
        pass

