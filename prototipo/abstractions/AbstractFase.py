from abc import ABC, abstractmethod


class AbstractFase(ABC):
    def __init__(self) -> None:
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