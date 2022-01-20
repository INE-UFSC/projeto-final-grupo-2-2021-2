from abc import ABC, abstractmethod
from Jogador import Jogador
from abstractions import AbstractTerreno


class AbstractFase(ABC):
    def __init__(self) -> None:
        pass

    @property
    @abstractmethod
    def terreno(self) -> AbstractTerreno:
        pass

    @property
    @abstractmethod
    def jogador(self) -> Jogador:
        pass

    @abstractmethod
    def ciclo(self) -> None:
        pass

    @abstractmethod
    def load(self) -> None:
        pass

    @abstractmethod
    def has_ended(self) -> bool:
        pass

    @abstractmethod
    def start(self) -> None:
        pass
