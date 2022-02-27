from abc import ABC, abstractmethod
from Personagens.Status import Status


class AbstractItem(ABC):
    @abstractmethod
    def modificar_status(self, status: Status) -> None:
        pass

    @abstractmethod
    def check_aplicado(self) -> bool:
        pass
