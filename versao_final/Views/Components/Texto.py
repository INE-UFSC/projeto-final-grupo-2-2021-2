import pygame
from Utils.Hitbox import Hitbox


class Texto:
    def __init__(self, posicao: tuple, tamanho: tuple, texto: str, font_size, color) -> None:
        self.__hitbox = Hitbox(posicao, tamanho)
        self.__input_text = texto
        self.__font = pygame.font.SysFont('cambria', font_size)
        self.__color = color

        self.__renderizar_texto()
        self.__text_rect = self.__text.get_rect(center=self.__hitbox.posicao)

    def desenhar(self, tela):
        tela.janela.blit(self.__text, self.__text_rect)

    def mudar_texto(self, texto):
        if type(texto) == str:
            self.__input_text = texto
            self.__renderizar_texto()

    def __renderizar_texto(self):
        self.__text = self.__font.render(self.__input_text, True, self.__color)

    @property
    def hitbox(self) -> Hitbox:
        return self.__hitbox
