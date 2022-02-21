import pygame
from Views.Components.Imagem import Imagem

BOTAO_IMAGEM_PATH = 'imagens/botao.png'


class Botao(Imagem):
    def __init__(self, posicao, tamanho, text, function, args=None) -> None:
        super().__init__(posicao, tamanho, BOTAO_IMAGEM_PATH)
        self.__input_text = text
        self.__font = pygame.font.SysFont('cambria', 27)
        self.__color = (0, 0, 0)

        self.__renderizar_texto()
        self.__text_rect = self.__text.get_rect(center=self.hitbox.posicao)
        
        self.__function = function
        self.__args = args

    def desenhar(self, tela):
        tela.janela.blit(self.imagem, self.rect)
        tela.janela.blit(self.__text, self.__text_rect)

    def execute(self):
        self.__function(self.__args)

    def mudar_texto(self, texto):
        if type(texto) == str:
            self.__input_text = texto
            self.__renderizar_texto()

    def __renderizar_texto(self):
        self.__text = self.__font.render(self.__input_text, True, self.__color)
