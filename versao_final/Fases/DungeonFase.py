from typing import List
from Mapas.AbstractMapa import AbstractMapa
from Personagens.Inimigos.ReaperAzul import ReaperAzul
from Personagens.Jogador import Jogador
from Config.Opcoes import Dificuldade, Opcoes
from Mapas.DungeonMap1 import DungeonMap1
from Mapas.DungeonMap2 import DungeonMap2
from Mapas.DungeonMap3 import DungeonMap3
from Personagens.Inimigos.MinotauroAzul import MinotauroAzul
from Personagens.Inimigos.MinotauroCinza import MinotauroCinza
from Personagens.Inimigos.MinotauroMarrom import MinotauroMarrom
from Personagens.Inimigos.ReaperVerde import ReaperVerde
from Fases.AbstractFase import AbstractFase
from Sounds.MusicHandler import MusicHandler


class DungeonFase(AbstractFase):
    def __init__(self, jogador: Jogador) -> None:
        self.__opcoes = Opcoes()
        self.__dificuldade = self.__opcoes.dificuldade
        self.__music = MusicHandler()

        first_enemies = self.__get_enemies_first_map()
        map1 = DungeonMap1(jogador, first_enemies)
        second_enemies = self.__get_enemies_second_map()
        map2 = DungeonMap2(jogador, second_enemies)
        third_enemies = self.__get_enemies_third_map()
        map3 = DungeonMap3(jogador, third_enemies)

        maps: List[AbstractMapa] = [map1, map2, map3]
        super().__init__(jogador, maps)

    def __get_enemies_first_map(self) -> list:
        enemies = []

        if self.__dificuldade == Dificuldade.facil:
            for _ in range(4):
                enemies.append(MinotauroAzul)
            for _ in range(2):
                enemies.append(MinotauroMarrom)

        if self.__dificuldade == Dificuldade.medio:
            for _ in range(4):
                enemies.append(MinotauroAzul)
            for _ in range(3):
                enemies.append(MinotauroMarrom)
            for _ in range(2):
                enemies.append(MinotauroCinza)

        elif self.__dificuldade == Dificuldade.dificil:
            for _ in range(4):
                enemies.append(MinotauroAzul)
            for _ in range(2):
                enemies.append(MinotauroMarrom)
            for _ in range(2):
                enemies.append(MinotauroCinza)
            for _ in range(1):
                enemies.append(ReaperAzul)

        return enemies

    def __get_enemies_second_map(self) -> list:
        enemies = []

        if self.__dificuldade == Dificuldade.facil:
            for _ in range(2):
                enemies.append(MinotauroAzul)
            for _ in range(1):
                enemies.append(MinotauroMarrom)
            for _ in range(2):
                enemies.append(ReaperAzul)

        if self.__dificuldade == Dificuldade.medio:
            for _ in range(3):
                enemies.append(MinotauroAzul)
            for _ in range(2):
                enemies.append(MinotauroMarrom)
            for _ in range(3):
                enemies.append(ReaperAzul)
            for _ in range(2):
                enemies.append(ReaperVerde)

        elif self.__dificuldade == Dificuldade.dificil:
            for _ in range(2):
                enemies.append(MinotauroAzul)
            for _ in range(2):
                enemies.append(MinotauroMarrom)
            for _ in range(2):
                enemies.append(ReaperAzul)
            for _ in range(3):
                enemies.append(ReaperVerde)

        return enemies

    def __get_enemies_third_map(self) -> list:
        enemies = []

        if self.__dificuldade == Dificuldade.facil:
            for _ in range(2):
                enemies.append(MinotauroAzul)
            for _ in range(1):
                enemies.append(MinotauroMarrom)
            for _ in range(2):
                enemies.append(ReaperAzul)

        if self.__dificuldade == Dificuldade.medio:
            for _ in range(2):
                enemies.append(MinotauroAzul)
            for _ in range(1):
                enemies.append(MinotauroMarrom)
            for _ in range(4):
                enemies.append(ReaperAzul)
            for _ in range(3):
                enemies.append(ReaperVerde)

        elif self.__dificuldade == Dificuldade.dificil:
            for _ in range(2):
                enemies.append(MinotauroAzul)
            for _ in range(2):
                enemies.append(MinotauroMarrom)
            for _ in range(2):
                enemies.append(ReaperAzul)
            for _ in range(3):
                enemies.append(ReaperVerde)

        return enemies
