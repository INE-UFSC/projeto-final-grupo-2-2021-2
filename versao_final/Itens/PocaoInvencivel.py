from Abstractions.AbstractItem import AbstractItem
from Personagens.Status import Status
import pygame

class PocaoInvencivel(AbstractItem):
    def __init__(self) -> None:
        self.__status: Status = None
        self.__pronto = False
        self.__aplicado = False
        self.__BUFF_TIMER = 80
        self.__imagem = pygame.image.load('imagens/pocao.png')
        self.__posicao = ()
    
    @property
    def imagem(self):
        return self.__imagem
    
    @imagem.setter
    def imagem(self, imagem):
        self.__imagem = imagem
    
    @property
    def posicao(self):
        return self.__posicao
    
    @posicao.setter
    def posicao(self, posicao):
        self.__posicao = posicao

    def adicionar_status(self, status: Status) -> None:
        pass

    def modificar_status(self, status: Status) -> None:
        if not self.__aplicado:
            self.__status = status
            self.__aplicado = True
            status.invencibilidade = True

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
