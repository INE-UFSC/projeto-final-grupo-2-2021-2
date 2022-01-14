from abc import abstractmethod, ABC
from abstractions.AbstractPersonagem import AbstractPersonagem


class AbstractInimigo(AbstractPersonagem, ABC):
    def __init__(self, stats: dict, posicao: tuple, tamanho: tuple) -> None:
        super().__init__(stats, posicao, tamanho)

    def mover():
        pass

    @abstractmethod
    def sprite_path(self) -> str:
        pass

    @abstractmethod
    def _calibrar_dificuldade(self):
        pass
