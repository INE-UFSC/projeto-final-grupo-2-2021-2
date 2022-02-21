import pygame
from Views.Components.Imagem import Imagem

BOTAO_IMAGEM_PATH = 'imagens/botao.png'


class Botao(Imagem):
    def __init__(self, posicao, tamanho, text, function) -> None:
        super().__init__(posicao, tamanho, BOTAO_IMAGEM_PATH)
        self.__input_text = text
        self.__font = pygame.font.SysFont('cambria', 27)
        self.__color = (0, 0, 0)

        self.__text = self.__font.render(self.__input_text, True, self.__color)
        self.__text_rect = self.__text.get_rect(center=self.hitbox.posicao)
        self.__function = function

    def desenhar(self, tela):
        tela.janela.blit(self.imagem, self.rect)
        tela.janela.blit(self.__text, self.__text_rect)

    def execute(self):
        self.__function()
