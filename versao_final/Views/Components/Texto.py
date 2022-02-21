import pygame
from Utils.Hitbox import Hitbox


class Texto:
    def __init__(self, posicao: tuple, tamanho: tuple, texto: str) -> None:
        self.__hitbox = Hitbox(posicao, tamanho)
        self.__input_text = texto
        self.__font = pygame.font.SysFont('cambria', 40)
        self.__color = (255, 255, 255)

        self.__text = self.__font.render(self.__input_text, True, self.__color)
        self.__text_rect = self.__text.get_rect(center=self.__hitbox.posicao)

    def desenhar(self, tela):
        self.__text_rect = self.__text.get_rect(center=self.__hitbox.posicao)
        tela.janela.blit(self.__text, self.__text_rect)

    @property
    def hitbox(self) -> Hitbox:
        return self.__hitbox
