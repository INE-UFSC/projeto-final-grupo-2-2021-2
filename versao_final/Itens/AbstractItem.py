from abc import ABC, abstractmethod
from pygame import Rect, Surface
from Personagens.Status import Status


class AbstractItem(ABC):
    @abstractmethod
    def modificar_status(self, status: Status) -> None:
        pass

    @abstractmethod
    def check_aplicado(self) -> bool:
        pass

    @abstractmethod
    def image(self) -> Surface:
        pass

    @abstractmethod
    def rect(self) -> Rect:
        pass

    @abstractmethod
    def posicao(self) -> None:
        pass
