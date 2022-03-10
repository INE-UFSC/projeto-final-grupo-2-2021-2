from random import choice
from typing import List, Type
from pygame import Rect, Surface
from Abstractions.AbstractInimigo import AbstractInimigo
from Abstractions.AbstractItem import AbstractItem
from Abstractions.AbstractTerreno import AbstractTerreno
from Itens.PocaoDefesa import PocaoDefesa
from Itens.PocaoMedia import PocaoMedia
from Itens.PocaoPequena import PocaoPequena
from Itens.PocaoVeneno import PocaoVeneno
from Personagens.Jogador.Jogador import Jogador
from Utils.Adapter import Adapter
from Utils.Folder import import_single_sprite
from random import random


class DungeonMap(AbstractTerreno):
    def __init__(self, jogador: Jogador, enemies_quant: int, enemies_types: List[Type[AbstractInimigo]]):
        self.__adapter = Adapter()
        self.__rooms = [matrix_dungeon1, matrix_dungeon2]
        self.__end_paths = ['sala1', 'sala2']

        self.__HAS_ENDED = False
        self.__enemies_quant = enemies_quant
        self.__enemies_types: List[Type[AbstractInimigo]] = enemies_types

        super().__init__([], jogador)
        self.__set_next_room()

        self.__itens: List[Type[AbstractItem]] = [PocaoDefesa, PocaoMedia, PocaoPequena]
        self.__itens_to_chance = {PocaoDefesa: 0.3,
                                  PocaoMedia: 0.15,
                                  PocaoPequena: 0.45,
                                  PocaoVeneno: 0.1}

    def update(self) -> None:
        if self.__has_ended_current_room():
            self.__set_next_room()

        super().update()

    def __set_next_room(self):
        if len(self.__rooms) > 0:
            room = self.__rooms.pop(0)
            end_path = self.__end_paths.pop(0)
            super()._setup_mapa(room)

            self.__SPRITE_PATH = f'Assets/Mapas/Dungeon/{end_path}.png'
            self.__image = import_single_sprite(self.__SPRITE_PATH, self._opcoes.TAMANHO_MAPAS)
            self.__rect = self.__image.get_rect(center=self.hitbox.center)

            inimigos = self.__criar_inimigos(self.__enemies_quant)
            self.load_inimigos(inimigos)
        else:
            self.__HAS_ENDED = True

    def __criar_inimigos(self, enemies_quant: int) -> List[AbstractInimigo]:
        enemies_list: List[AbstractInimigo] = []

        for _ in range(enemies_quant):
            position = self._room.get_random_enemy_position()
            position = self.__adapter.matrix_index_to_pygame_pos(position)

            Enemy_Type = choice(self.__enemies_types)
            enemy = Enemy_Type(terreno=self, posicao=position)
            enemies_list.append(enemy)

        return enemies_list

    def _get_item_to_drop(self) -> AbstractItem:
        for item in self.__itens:
            chance = self.__itens_to_chance[item]
            if chance > random():
                return item()

    def __has_ended_current_room(self) -> bool:
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

    def has_ended(self) -> bool:
        return self.__HAS_ENDED


matrix_dungeon1 = [
    #          X         X         X         X
    # 01234567890123456789012345678901234567890123456
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',  # 0
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',  # 1
    'PP00      00PP00                PP0          PP',  # 2
    'PP        00PP00                PP  5        PP',  # 3
    'PP    5     PP     5   5   5    PP           PP',  # 4
    'PP          PP                  PP       5   PP',  # 5
    'PP   5      PP                  PP           PP',  # 6
    'PP         0PP                  PP           PP',  # 7
    'PP5   PPPPPPPP                  PP   PPPPPPPPPP',  # 8
    'PP    PPPPPPPP                  PP   PPPPPPPPPP',  # 9c
    'PP         0PP      5                        PP',  # 10
    'PP    5     PP                            5  PP',  # 11
    'PP          PP      PPPPPPPP 5               PP',  # 12
    'PP          PP      PPPPPPPP              5  PP',  # 13
    'PP 5        PP      PPPPPPPP                 PP',  # 14
    'PP        00PP      PPPPPPPP 5       PPPPPPPPPP',  # 15
    'PP    PPPPPPPP      PPPPPPPP         PPPPPPPPPP',  # 16
    'PP    PPPPPPPP      PPPPPPPP         PPPPPPPPPP',  # 17
    'PP                     PP            PPPPPPPPPP',  # 18
    'PP     5       5       PP            P J     PP',  # 19
    'PP                     PP            P       PP',  # 20
    'PP             000     PP                    PP',  # 21
    'PP    5        000     PP                  00PP',  # 22
    'PP             000     PP                  00PP',  # 23
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',  # 24
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP']  # 25

matrix_dungeon2 = [
    #          X         X         X         X
    # 01234567890123456789012345678901234567890123456
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',  # 0
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',  # 1
    'PPPPPPPPPP                   000PP        0 0PP',  # 2
    'PPPPPPPPPP                      PP 5      0 0PP',  # 3
    'PPPPPPPPPP         5            PP     5     PP',  # 4
    'PPPPPPPPPP                      PP 5         PP',
    'PP                              PP           PP',  # 6
    'PP                 5            PP          0PP',  # 7
    'PP                              PP   PPPPPPPPPP',  # 8
    'PP                              PP   PPPPPPPPPP',  # 9c
    'PP         PPPPPPPPPPPPPP                    PP',  # 10
    'PP  5  5   PPPPPPPPPPPPPP                    PP',  # 11
    'PP         PP00      5                       PP',  # 12
    'PP         PP0    5                           PP',  # 13
    'PP         PP                                PP',  # 14
    'PP         PP  5     5          PPPPPPPPPPPPPPPP',  # 1
    'PP         PP     000           PPPPPPPPPPPPPPP',  # 16
    'PP         PP     000   P       PPPPPPPPPPPPPPP',  # 17
    'PP         PP 5   000   P       PPPPPPPPPPPPPPP',  # 18
    'PP         PP           P       P   5        PP',  # 19
    'PP         PP           P       P      5     PP',  # 20
    'PP   J     PP     5     P                    PP',  # 21
    'PPPP       PP00         P          5         PP',  # 22
    'PPPP       PP00         P                    PP',  # 23
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',  # 24
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP']  # 25


# A parede no canto inferior direito fica nos quadrados 46x25
