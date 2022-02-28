from Abstractions.AbstractObstaculo import AbstractObstaculo
from Utils.Folder import import_single_sprite
from pygame import Surface, Rect


class Parede(AbstractObstaculo):
    __SPRITES_CARREGADOS = False
    __SPRITE_PATH = ''
    __SPRITE: Surface = {}
    __TAMANHO = (32, 32)

    def __init__(self, posicao: tuple, tamanho: tuple) -> None:
        super().__init__(posicao=posicao, tamanho=tamanho, transpassavel=False)

        if not Parede.__SPRITES_CARREGADOS:
            Parede.__import_sprites()
            Parede.__SPRITES_CARREGADOS = True

        self.__image = Parede.__SPRITE
        self.__rect = self.__image.get_rect(center=self.hitbox.center)

    @property
    def image(self) -> Surface:
        return self.__image

    @property
    def rect(self) -> Rect:
        return self.__rect

    @classmethod
    def __import_sprites(cls):
        cls.__SPRITE = import_single_sprite(cls.__SPRITE_PATH, cls.__TAMANHO)
