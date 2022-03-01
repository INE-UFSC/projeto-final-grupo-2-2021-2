from Abstractions.AbstractItem import AbstractItem
from Personagens.Status import Status
import pygame


class PocaoDefesa(AbstractItem):
    def __init__(self) -> None:
        self.__potencia = 3
        self.__aplicado = False
        self.__imagem = pygame.image.load('Assets/pocoes/pocao_defesa.png')
        self.__posicao = ()
    
    @property
    def imagem(self):
        return self.__imagem
    
    @property
    def posicao(self):
        return self.__posicao
    
    @posicao.setter
    def posicao(self, posicao):
        self.__posicao = posicao
    
    def modificar_status(self, status: Status) -> None:
        if not self.__aplicado:
            status.defesa += self.__potencia
            self.__aplicado = True

    def check_aplicado(self) -> bool:
        return True

