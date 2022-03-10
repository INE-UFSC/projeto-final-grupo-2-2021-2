from random import choice
from typing import List, Type
from pygame import Rect, Surface
from Personagens.Inimigos.AbstractInimigo import AbstractInimigo
from Itens.AbstractItem import AbstractItem
from Terrenos.AbstractTerreno import AbstractTerreno
from Itens.Pocoes.PocaoDefesa import PocaoDefesa
from Itens.Pocoes.PocaoMedia import PocaoMedia
from Itens.Pocoes.PocaoPequena import PocaoPequena
from Itens.Pocoes.PocaoVeneno import PocaoVeneno
from Personagens.Jogador import Jogador
from Utils.Adapter import Adapter
from Utils.Folder import import_single_sprite
from random import random


class DungeonMap(AbstractTerreno):
    def __init__(self, jogador: Jogador, enemies_quant: int, enemies_types: List[Type[AbstractInimigo]]):
        self.__adapter = Adapter()
        self.__jogador = jogador
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
        if self.__logic_room_ended():
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

    def __all_enemies_dead(self) -> bool:
        for inimigo in self.inimigos:
            if not inimigo.morreu:
                return False
        return True

    def __logic_room_ended(self) -> bool:
        if not self.__all_enemies_dead():
            return False

        rect_jogador = Rect(self.__jogador.hitbox.posicao, self.__jogador.hitbox.tamanho)
        posicao_end_matrix = self._room.position_end_room
        posicao_end_screen = self.__adapter.matrix_index_to_pygame_pos(posicao_end_matrix)

        if rect_jogador.collidepoint(posicao_end_screen):
            return True

        return False

    @property
    def image(self) -> Surface:
        return self.__image

    @property
    def rect(self) -> Rect:
        return self.__rect

    def has_ended(self) -> bool:
        return self.__HAS_ENDED


matrix_dungeon1 = [
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',
    'PP00      00PP00                PP0          PP',
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
    'PP     5       5       PP            P J     PP',
    'PP                     PP            P       PP',
    'PP             000     PP                    PP',
    'PP    5        000     PP                  00PP',
    'PP             000     PP                  00PP',
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP']

matrix_dungeon2 = [
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',
    'PPPPPPPPPP                   000PP        000PP',
    'PPPPPPPPPP                      PP 5      000PP',
    'PPPPPPPPPP         5            PP     5   E PP',
    'PPPPPPPPPP                      PP 5         PP',
    'PP                              PP           PP',
    'PP                 5            PP          0PP',
    'PP                              PP   PPPPPPPPPP',
    'PP  5  5                        PP   PPPPPPPPPP',
    'PP         PPPPPPPPPPPPPP                    PP',
    'PP         PPPPPPPPPPPPPP                    PP',
    'PP         PP00      5                       PP',
    'PP         PP0    5                          PP',
    'PP         PP                                PP',
    'PP         PP  5     5          PPPPPPPPPPPPPPP',
    'PP         PP     000           PPPPPPPPPPPPPPP',
    'PP         PP     000   P       PPPPPPPPPPPPPPP',
    'PP         PP 5   000   P       PPPPPPPPPPPPPPP',
    'PP         PP           P       P   5        PP',
    'PP         PP           P       P      5     PP',
    'PP   J     PP     5     P                    PP',
    'PPPP       PP00         P          5         PP',
    'PPPP       PP00         P                    PP',
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP']


# A parede no canto inferior direito fica nos quadrados 46x25
