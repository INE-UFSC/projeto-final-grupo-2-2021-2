from typing import List, Type
from pygame import K_e, Rect, Surface, key
from Personagens.AbstractInimigo import AbstractInimigo
from Itens.AbstractItem import AbstractItem
from Mapas.AbstractMapa import AbstractMapa
from Itens.Pocoes.PocaoForca import PocaoForca
from Itens.Pocoes.PocaoDefesa import PocaoDefesa
from Itens.Pocoes.PocaoMedia import PocaoMedia
from Itens.Pocoes.PocaoPequena import PocaoPequena
from Itens.Pocoes.PocaoVeneno import PocaoVeneno
from Itens.Pocoes.PocaoVelocidade import PocaoVelocidade
from Personagens.Jogador import Jogador
from Utils.Adapter import Adapter
from Utils.Folder import import_single_sprite
from random import random


class DungeonMap1(AbstractMapa):
    __MATRIX = [
        'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',
        'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',
        'PP        00PP00                PP0          PP',
        'PP E      00PP00                PP  5        PP',
        'PP    5     PP     5   5   5    PP           PP',
        'PP          PP                  PP       5   PP',
        'PP   5      PP                  PP           PP',
        'PP         0PP                  PP           PP',
        'PP5   PPPPPPPP                  PP   PPPPPPPPPP',
        'PP    PPPPPPPP                  PP   PPPPPPPPPP',
        'PP         0PP      5                        PP',
        'PP    5     PP                            5  PP',
        'PP          PP      PPPPPPPP 5               PP',
        'PP          PP      PPPPPPPP              5  PP',
        'PP 5        PP      PPPPPPPP                 PP',
        'PP        00PP      PPPPPPPP 5       PPPPPPPPPP',
        'PP    PPPPPPPP      PPPPPPPP         PPPPPPPPPP',
        'PP    PPPPPPPP      PPPPPPPP         PPPPPPPPPP',
        'PP                     PP            PPPPPPPPPP',
        'PP     5       5       PP            P       PP',
        'PP                     PP            P       PP',
        'PP             000     PP                  I PP',
        'PP    5        000     PP                J 00PP',
        'PP             000     PP                  00PP',
        'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',
        'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP']
    __SPRITE_PATH = 'Assets/Mapas/Dungeon/sala1.png'

    def __init__(self, jogador: Jogador, enemies: List[Type[AbstractInimigo]]):
        super().__init__(jogador, enemies)

        self.__adapter = Adapter()

        self.__image = self.__import_background()
        self.__rect = self.__image.get_rect(center=self.hitbox.center)

        self.__itens_to_chance = {PocaoDefesa: 0.10, PocaoMedia: 0.10, PocaoPequena: 0.35,
                                  PocaoVeneno: 0.10, PocaoVelocidade: 0.15, PocaoForca: 0.10}

        self.__GO_NEXT_MAP = False
        self.__GO_PREVIOUS_MAP = False
        self.__LOADED = False

    def load(self) -> None:
        if not self.__LOADED:
            super()._setup_mapa(DungeonMap1.__MATRIX)
            super().load()
            self.__LOADED = True

    def update(self) -> None:
        if self.__all_enemies_dead():
            position_end_map = self._map.end_map_position
            position_end_map = self.__adapter.matrix_index_to_pygame_pos(position_end_map)

            keys = key.get_pressed()
            rect_jogador = Rect(self.jogador.hitbox.posicao, self.jogador.hitbox.tamanho)
            if rect_jogador.collidepoint(position_end_map):
                if keys[K_e]:
                    self.__GO_NEXT_MAP = True

        super().update()

    def __import_background(self) -> Surface:
        return import_single_sprite(self.__SPRITE_PATH, self._opcoes.TAMANHO_MAPAS)

    def _get_item_to_drop(self) -> AbstractItem:
        for item in self.__itens_to_chance.keys():
            chance = self.__itens_to_chance[item]
            if chance > random():
                return item()

    def __all_enemies_dead(self) -> bool:
        for inimigo in self.inimigos:
            if not inimigo.morreu:
                return False
        return True

    @property
    def image(self) -> Surface:
        return self.__image

    @property
    def rect(self) -> Rect:
        return self.__rect

    @property
    def go_next_map(self) -> bool:
        if self.__GO_NEXT_MAP:
            self.__GO_NEXT_MAP = False
            return True
        else:
            return False

    @property
    def go_previous_map(self) -> bool:
        if self.__GO_PREVIOUS_MAP:
            self.__GO_PREVIOUS_MAP = False
            return True
        else:
            return False

    @property
    def loaded(self) -> bool:
        return self.__LOADED
