from Itens.AbstractItem import AbstractItem
from pygame import Surface
from Utils.Folder import import_single_sprite


class PocaoGenerica(AbstractItem):
    __PATH_TO_SPRITE = {}
    __SIZE_TO_SPRITE = {}

    def __init__(self, path: str, size: tuple) -> None:
        if path not in PocaoGenerica.__PATH_TO_SPRITE or size not in PocaoGenerica.__SIZE_TO_SPRITE:
            self.__image = self.__load_image(path, size)
            PocaoGenerica.__PATH_TO_SPRITE[path] = self.__image
            PocaoGenerica.__SIZE_TO_SPRITE[size] = self.__image
        else:
            self.__image = self.__PATH_TO_SPRITE[path]

    def _get_image(self) -> Surface:
        return self.__image

    @classmethod
    def __load_image(cls, path: str, size: tuple) -> Surface:
        return import_single_sprite(path, size)
