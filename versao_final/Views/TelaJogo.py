import pygame
from Config.Config import TAMANHO_TELA

BACKGROUND_PATH = 'imagens/capa.png'
GAME_TITLE = 'The Binding of Isaac'


class TelaJogo():
    def __init__(self) -> None:
        self.__tamanho = TAMANHO_TELA
        self.__janela = pygame.display.set_mode(self.__tamanho)

        imagem_fundo = pygame.image.load(BACKGROUND_PATH)
        self.__plano_fundo = pygame.transform.scale(imagem_fundo, self.__tamanho)

        pygame.display.set_caption(GAME_TITLE)

    @property
    def tamanho(self) -> int:
        return self.__tamanho

    @tamanho.setter
    def tamanho(self, tamanho) -> tuple:
        if type(tamanho) == tuple:
            self.__tamanho = tamanho

    @property
    def janela(self) -> pygame.surface:
        return self.__janela

    def mostrar_fundo(self) -> None:
        return self.janela.blit(self.__plano_fundo, (0, 0))
