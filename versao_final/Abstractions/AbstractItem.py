from abc import ABC, abstractmethod


class AbstractItem(ABC):
    @abstractmethod
    def vida(self, vida_atual):
        pass

    @abstractmethod
    def velocidade(self, velocidade):
        pass

    @abstractmethod
    def defesa(self, defesa):
        pass

    @abstractmethod
    def vida_maxima(self, vida_maxima):
        pass

    @abstractmethod
    def dano(self, dano):
        pass

    @abstractmethod
    def velocidade(self, velocidade):
        pass

    @abstractmethod
    def invencibilidade(self) -> bool:
        pass
