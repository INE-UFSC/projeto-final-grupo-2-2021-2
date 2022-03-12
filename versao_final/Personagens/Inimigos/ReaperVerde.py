from Personagens.InimigoTipo1 import InimigoTipo1
from Mapas.AbstractMapa import AbstractMapa


class ReaperVerde(InimigoTipo1):
    __TAMANHO_IMAGEM = (80, 80)
    __TAMANHO = (35, 45)
    __SPRITE_PATH = 'Assets/Personagens/Reaper/ReaperVerde/'
    __STATS_FACIL = {'vida': 15, 'ataque': 4, 'defesa': 3, 'vel': 2, 'vel_ataque': 1, 'arma_dano': 3,
                     'arma_alcance': 18, 'view_distance': 150, 'transpassavel': False}
    __STATS_MEDIO = {'vida': 20, 'ataque': 5, 'defesa': 4, 'vel': 2, 'vel_ataque': 1, 'arma_dano': 4,
                     'arma_alcance': 18, 'view_distance': 150, 'transpassavel': False}
    __STATS_DIFICIL = {'vida': 25, 'ataque': 6, 'defesa': 5, 'vel': 3, 'vel_ataque': 1, 'arma_dano': 5,
                       'arma_alcance': 18, 'view_distance': 150, 'transpassavel': False}
    __DIST_PARA_ATAQUE = 8
    __CHANCE_DAMAGE_STOP_ATTACK = 0.5
    __FRAME_EXECUTAR_ATAQUE = 17

    def __init__(self, mapa: AbstractMapa, posicao=(0, 0)) -> None:
        super().__init__(mapa, ReaperVerde.__SPRITE_PATH, posicao)

    @property
    def _SPRITE_PATH(self) -> str:
        return ReaperVerde.__SPRITE_PATH

    @property
    def _STATS_DIFICIL(self) -> dict:
        return ReaperVerde.__STATS_DIFICIL

    @property
    def _STATS_FACIL(self) -> dict:
        return ReaperVerde.__STATS_FACIL

    @property
    def _STATS_MEDIO(self) -> dict:
        return ReaperVerde.__STATS_MEDIO

    @property
    def _TAMANHO(self) -> tuple:
        return ReaperVerde.__TAMANHO

    @property
    def _TAMANHO_IMAGEM(self) -> tuple:
        return ReaperVerde.__TAMANHO_IMAGEM

    @property
    def _CHANCE_DAMAGE_STOP_ATTACK(self) -> float:
        return ReaperVerde.__CHANCE_DAMAGE_STOP_ATTACK

    @property
    def _DIST_PARA_ATAQUE(self) -> tuple:
        return ReaperVerde.__DIST_PARA_ATAQUE

    @property
    def _FRAME_EXECUTAR_ATAQUE(self) -> int:
        return ReaperVerde.__FRAME_EXECUTAR_ATAQUE