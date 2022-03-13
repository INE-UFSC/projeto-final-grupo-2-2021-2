from abc import ABC, abstractmethod
from pygame import Rect
from Config.Enums import Direction
from Utils.Hitbox import Hitbox


class AbstractEscudo(ABC):
    @abstractmethod
    def __init__(self, player_hitbox: Hitbox) -> None:
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def tomar_dano(self, dano) -> int:
        pass

    @abstractmethod
    def get_rect(self, direction: Direction) -> Rect:
        pass

    @property
    @abstractmethod
    def vida_maxima(self) -> int:
        pass

    @property
    @abstractmethod
    def vida(self) -> int:
        pass

    @property
    @abstractmethod
    def defesa(self) -> int:
        pass

    @property
    @abstractmethod
    def quebrado(self) -> bool:
        pass

    @property
    @abstractmethod
    def movement_slow(self) -> int:
        pass
