from pygame import Rect, Surface
from Config.Opcoes import Opcoes
from Config.TelaJogo import TelaJogo
from Personagens.Status import Status
from Utils.Folder import import_single_sprite


class HUD:
    __PATH = 'Assets/HUD/Fundo.png'
    __SIZE = Opcoes().TAMANHO_HUD

    def __init__(self, status: Status) -> None:
        self.__status = status
        self.__posicao = Opcoes().POSICAO_HUD
        self.__image = import_single_sprite(HUD.__PATH, HUD.__SIZE)
        self.__rect = self.__image.get_rect(topleft=self.__posicao)

    def image(self) -> Surface:
        return self.__image

    def rect(self) -> Rect:
        return self.__rect

    def update(self) -> None:
        pass

    def desenhar(self, tela: TelaJogo):
        tela.janela.blit(self.__image, self.__rect)
