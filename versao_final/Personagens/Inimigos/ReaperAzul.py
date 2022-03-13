from Personagens.InimigoTipo1 import InimigoTipo1
from Mapas.AbstractMapa import AbstractMapa


class ReaperAzul(InimigoTipo1):
    __TAMANHO_IMAGEM = (80, 80)
    __TAMANHO = (35, 45)
    __SPRITE_PATH = 'Assets/Personagens/Reaper/ReaperAzul/'
    __STATS_FACIL = {'vida': 12, 'ataque': 3, 'defesa': 3, 'vel': 2, 'vel_ataque': 1,
                     'view_distance': 100, 'transpassavel': False}
    __STATS_MEDIO = {'vida': 18, 'ataque': 4, 'defesa': 4, 'vel': 2, 'vel_ataque': 1,
                     'view_distance': 100, 'transpassavel': False}
    __STATS_DIFICIL = {'vida': 23, 'ataque': 5, 'defesa': 5, 'vel': 3, 'vel_ataque': 1,
                       'view_distance': 100, 'transpassavel': False}
    __DIST_PARA_ATAQUE = 7
    __CHANCE_DAMAGE_STOP_ATTACK = 0.2
    __FRAME_EXECUTAR_ATAQUE = 17

    def __init__(self, mapa: AbstractMapa, posicao=(0, 0)) -> None:
        super().__init__(mapa, ReaperAzul.__SPRITE_PATH, posicao)

    @property
    def _SPRITE_PATH(self) -> str:
        return ReaperAzul.__SPRITE_PATH

    @property
    def _STATS_DIFICIL(self) -> dict:
        return ReaperAzul.__STATS_DIFICIL

    @property
    def _STATS_FACIL(self) -> dict:
        return ReaperAzul.__STATS_FACIL

    @property
    def _STATS_MEDIO(self) -> dict:
        return ReaperAzul.__STATS_MEDIO

    @property
    def _TAMANHO(self) -> tuple:
        return ReaperAzul.__TAMANHO

    @property
    def _TAMANHO_IMAGEM(self) -> tuple:
        return ReaperAzul.__TAMANHO_IMAGEM

    @property
    def _CHANCE_DAMAGE_STOP_ATTACK(self) -> float:
        return ReaperAzul.__CHANCE_DAMAGE_STOP_ATTACK

    @property
    def _DIST_PARA_ATAQUE(self) -> tuple:
        return ReaperAzul.__DIST_PARA_ATAQUE

    @property
    def _FRAME_EXECUTAR_ATAQUE(self) -> int:
        return ReaperAzul.__FRAME_EXECUTAR_ATAQUE
