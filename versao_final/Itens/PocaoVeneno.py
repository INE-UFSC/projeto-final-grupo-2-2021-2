from Abstractions.AbstractItem import AbstractItem
from Personagens.Status import Status
import pygame


class PocaoVeneno(AbstractItem):
    def __init__(self) -> None:
        self.__status: Status = None
        self.__potencia = 3
        self.__pronto = False
        self.__aplicado = False
        self.__BUFF_TIMER = 100
        self.__imagem = pygame.image.load('Assets/pocoes/pocao_veneno.png')
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
        self.__status = status
        if not self.__aplicado:
            status.vel -= self.__potencia
            status.vida -= self.__potencia
            self.__aplicado = True


    def check_aplicado(self) -> bool:
        if self.__pronto:
            self.__remover_status()
            return True
        else:
            self.__update_timer()

    def __remover_status(self) -> None:
        if self.__pronto:
            self.__status.vel += self.__potencia
            self.__pronto = False
        
    def __update_timer(self):
        if self.__BUFF_TIMER > 0:
            self.__BUFF_TIMER -= 1
        else:
            self.__pronto = True
        