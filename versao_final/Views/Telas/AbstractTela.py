from abc import ABC, abstractmethod


class AbstractTela(ABC):
    @abstractmethod
    def run(self):
        pass
