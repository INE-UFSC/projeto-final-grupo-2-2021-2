from Abstractions.AbstractItem import AbstractItem
from Personagens.Status import Status


class PocaoPequena(AbstractItem):
    def __init__(self) -> None:
        self.__potencia = 3
        self.__pronto = False

    def adicionar_status(self, status: Status) -> None:
        if not self.__pronto:
            status.vida += self.__potencia
            self.__pronto = True

    def check_aplicado(self) -> bool:
        return self.__pronto
