from Abstractions.AbstractItem import AbstractItem
from Personagens.Status import Status


class PocaoMedia(AbstractItem):
    def __init__(self) -> None:
        self.__potencia = 5
        self.__pronto = False

    def adicionar_status(self, status: Status) -> None:
        status.vida += self.__potencia
        self.__pronto = True

    def check_aplicado(self) -> bool:
        return self.__pronto
