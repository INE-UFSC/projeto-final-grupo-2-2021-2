import pygame
from Utils.Hitbox import Hitbox


class Imagem:
    def __init__(self, posicao: tuple, tamanho: tuple, path_imagem: str) -> None:
        self.__hitbox = Hitbox(posicao, tamanho)
        self.__load_imagem(path_imagem)

    def desenhar(self, tela):
        self.__rect = self.__imagem.get_rect(center=self.__hitbox.posicao)
        tela.janela.blit(self.__imagem, self.__rect)

    def __load_imagem(self, path):
        imagem = pygame.image.load(path)
        self.__imagem = pygame.transform.scale(imagem, self.__hitbox.tamanho)
        self.__rect = self.__imagem.get_rect(center=self.__hitbox.posicao)

    @property
    def hitbox(self) -> Hitbox:
        return self.__hitbox

    @property
    def imagem(self) -> pygame.Surface:
        return self.__imagem

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect
