from typing import List, Type
from Mapas.AbstractMapa import AbstractMapa
from Personagens.Inimigos.ReaperAzul import ReaperAzul
from Personagens.Jogador import Jogador
from Config.Opcoes import Dificuldade, Opcoes
from Mapas.DungeonMap1 import DungeonMap1
from Mapas.DungeonMap2 import DungeonMap2
from Personagens.Inimigos.MinotauroAzul import MinotauroAzul
from Personagens.Inimigos.MinotauroCinza import MinotauroCinza
from Personagens.Inimigos.MinotauroMarrom import MinotauroMarrom
from Personagens.Inimigos.ReaperVerde import ReaperVerde
from Fases.AbstractFase import AbstractFase


class DungeonFase(AbstractFase):
    def __init__(self, jogador: Jogador) -> None:
        self.__opcoes = Opcoes()
        self.__dificuldade = self.__opcoes.dificuldade

        first_enemies = self.__get_enemies_first_room()
        map1 = DungeonMap1(jogador, first_enemies)
        second_enemies = self.__get_enemies_second_room()
        map2 = DungeonMap2(jogador, second_enemies)

        maps: List[AbstractMapa] = [map1, map2]
        super().__init__(jogador, maps)

    def __get_enemies_first_room(self) -> list:
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

    def __get_enemies_second_room(self) -> list:
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
