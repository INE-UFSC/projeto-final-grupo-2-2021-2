from Itens.PocaoGenerica import PocaoGenerica
from Personagens.Status import Status
from pygame import Rect, Surface


class PocaoDefesa(PocaoGenerica):
    __PATH = 'Assets/pocoes/pocao_defesa.png'
    __SIZE = (30, 30)

    def __init__(self, position=(0, 0)) -> None:
        super().__init__(PocaoDefesa.__PATH, PocaoDefesa.__SIZE)
        self.__potencia = 3
        self.__aplicado = False
        self.__posicao = position
        self.__image = self._get_image()
        self.__rect = self.__image.get_rect(center=self.__posicao)

    @property
    def image(self) -> Surface:
        return self.__image

    @property
    def rect(self) -> Rect:
        return self.__rect

    @property
    def posicao(self) -> tuple:
        return self.__posicao

    @posicao.setter
    def posicao(self, posicao) -> tuple:
        self.__posicao = posicao
        self.__rect = self.__image.get_rect(center=self.__posicao)

    def modificar_status(self, status: Status) -> None:
        if not self.__aplicado:
            status.defesa += self.__potencia
            self.__aplicado = True

    def check_aplicado(self) -> bool:
        return True
