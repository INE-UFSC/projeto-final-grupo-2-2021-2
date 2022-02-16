from Abstractions.AbstractItem import AbstractItem
from Personagens.Status import Status


class PocaoDefesa(AbstractItem):
    def __init__(self) -> None:
        self.__status: Status = None
        self.__potencia = 3
        self.__pronto = False
        self.__BUFF_TIMER = 200

    def modificar_status(self, status: Status) -> None:
        self.__status = status
        status.defesa += self.__potencia

    def check_aplicado(self) -> bool:
        self.__update_timer()
        return self.__pronto

    def __remover_status(self) -> None:
        self.__status.invencibilidade = False

    def __update_timer(self):
        if self.__BUFF_TIMER > 0:
            self.__BUFF_TIMER -= 1
        else:
            self.__remover_status()
            self.__pronto = True
