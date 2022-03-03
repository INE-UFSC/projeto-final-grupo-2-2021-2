from typing_extensions import Self
from pygame import Rect, Surface
from Abstractions.AbstractItem import AbstractItem
from Abstractions.AbstractTerreno import AbstractTerreno
from Itens.PocaoDefesa import PocaoDefesa
from Itens.PocaoMedia import PocaoMedia
from Itens.PocaoPequena import PocaoPequena
from Obstaculos.ObstaculoInvisivel import ObjetoInvisivel
from Utils.Folder import import_single_sprite
from random import random


class DungeonMap(AbstractTerreno):
    __SPRITE_PATH = 'Assets/Mapas/Dungeon/fundo.png'
    __POSICAO_INICIAL_JOGADOR = (650, 650)

    def __init__(self, inimigos: list, jogador):
        super().__init__(inimigos, jogador)

        super()._setup_mapa(terreno)
        DungeonMap.__setup_mapa(self)

        self.__image = import_single_sprite(DungeonMap.__SPRITE_PATH, self._opcoes.TAMANHO_MAPAS)
        self.__rect = self.__image.get_rect(center=self.hitbox.center)
        self.__itens_e_chances = [(PocaoDefesa, 0.1), (PocaoMedia, 0.15), (PocaoPequena, 0.35)]

    @classmethod
    def __setup_mapa(cls, self: Self) -> None:
        self.jogador.hitbox.posicao = cls.__POSICAO_INICIAL_JOGADOR
        menor = self._opcoes.MENOR_UNIDADE

        for index_x, linha in enumerate(terreno):
            for index_y, cell in enumerate(linha):
                if cell != ' ':
                    posicao = self._aumentar_ponto((index_x, index_y))
                    posicao = self._inverter_ponto(posicao)
                    posicao = self._apply_offset_to_point(posicao)

                    if cell == 'P':
                        self.objetos.append(
                            ObjetoInvisivel(posicao, (menor, menor), False, True))
                    elif cell == '0':
                        self.objetos.append(
                            ObjetoInvisivel(posicao, (menor, menor), False, False))
                    elif cell == '1':
                        self.objetos.append(
                            ObjetoInvisivel(posicao, (menor, menor), True, True))
                    elif cell == '2':
                        self.objetos.append(
                            ObjetoInvisivel(posicao, (menor, menor), False, False))

    def __add_animated_objects(self):
        pass

    def _get_item_to_drop(self) -> AbstractItem:
        for item_chance in self.__itens_e_chances:
            chance = item_chance[1]
            item = item_chance[0]
            if chance > random():
                return item()

    @property
    def image(self) -> Surface:
        return self.__image

    @property
    def rect(self) -> Rect:
        return self.__rect

    def has_ended(self) -> bool:
        for inimigo in self.inimigos:
            if not inimigo.morreu:
                return False
        return True

    def _posicao_bloqueia_movimento(self, posicao: tuple) -> bool:
        posicao = self._remove_offset_from_point(posicao)
        posicao = self._reduzir_ponto(posicao)
        posicao = self._inverter_ponto(posicao)

        x = int(posicao[0])
        y = int(posicao[1])

        try:
            valor = terreno[x][y]
            if valor == 'P' or valor == '0':
                return True
            else:
                return False

        except Exception as e:
            print(f'Bloqueia Movimento - Acesso indevido a matriz em [{x}][{y}] - 3')
            return True

    def _posicao_bloqueia_visao(self, posicao: tuple) -> bool:
        posicao = self._remove_offset_from_point(posicao)
        posicao = self._reduzir_ponto(posicao)
        posicao = self._inverter_ponto(posicao)

        x = int(posicao[0])
        y = int(posicao[1])

        try:
            valor = terreno[x][y]
            if valor == 'P' or valor == '1':
                return True
            else:
                return False

        except Exception as e:
            print(f'Bloqueia Visão - Acesso indevido a matriz em [{x}][{y}] - 3')
            return True

    def _posicao_index_valido(self, posicao: tuple) -> bool:
        posicao = self._remove_offset_from_point(posicao)
        posicao = self._reduzir_ponto(posicao)
        posicao = self._inverter_ponto(posicao)

        x = int(posicao[0])
        y = int(posicao[0])

        if x < 0 or x >= len(terreno):
            print(f'Acesso indevido a matriz em [{x}][{y}] - 3')
            return False

        if y < 0 or y >= len(terreno[0]):
            print(f'Acesso indevido a matriz em [{x}][{y}] - 4')
            return False

        return True

# 1128x624
# 47x26
# P => Objeto não transpassavel,  bloqueia visão
# 0 => Objeto não transpassavel, não bloqueia visão
# 1 => Objeto transpassavel, bloqueia visão
# 2 => Objeto transpassavel, não bloqueia visão


terreno = [
    #          X         X         X         X
    # 01234567890123456789012345678901234567890123456
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',  # 0
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',  # 1
    'PP        00PP                               PP',  # 2
    'PP        00PP                               PP',  # 3
    'PP          PP                               PP',  # 4
    'PP          PP                               PP',  # 5
    'PP          PP                               PP',  # 6
    'PP         0PP                               PP',  # 7
    'PP    PPPPPPPP                               PP',  # 8
    'PP    PPPPPPPP                               PP',  # 9
    'PP    0    0PP                               PP',  # 10
    'PP          PP                               PP',  # 11
    'PP          PP                               PP',  # 12
    'PP          PP                               PP',  # 13
    'PP          PP                               PP',  # 14
    'PP         0PP                               PP',  # 15
    'PP    PPPPPPPP                               PP',  # 16
    'PP    PPPPPPPP                               PP',  # 17
    'PP                                           PP',  # 18
    'PP                                           PP',  # 19
    'PP                                           PP',  # 20
    'PP                                           PP',  # 21
    'PP                                           PP',  # 22
    'PP                                           PP',  # 23
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',  # 24
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP']  # 25

# A parede no canto inferior direito fica nos quadrados 46x25
