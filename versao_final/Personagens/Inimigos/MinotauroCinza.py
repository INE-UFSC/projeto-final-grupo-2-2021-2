from Personagens.InimigoTipo1 import InimigoTipo1
from Mapas.AbstractMapa import AbstractMapa
from random import choice


class MinotauroCinza(InimigoTipo1):
    __TAMANHO_IMAGEM = (80, 65)
    __TAMANHO = (30, 42)
    __SPRITE_PATH = 'Assets/Personagens/Minotauro/MinotauroCinza/'
    __HURT_SOUND_END_PATHS = ['ogre1.wav', 'ogre2.wav', 'ogre3.wav', 'ogre4.wav', 'ogre5.wav']
    __DYING_SOUND_PATH = 'Sounds/sounds/Monsters/Die/ogre2.wav'
    __HURT_SOUNDS_PATH_BASE = 'Sounds/sounds/Monsters/Hurt/'
    __STATS_FACIL = {'vida': 15, 'ataque': 4, 'defesa': 3, 'vel': 2, 'vel_ataque': 1,
                     'view_distance': 150, 'transpassavel': False}
    __STATS_MEDIO = {'vida': 20, 'ataque': 5, 'defesa': 4, 'vel': 2, 'vel_ataque': 1,
                     'view_distance': 150, 'transpassavel': False}
    __STATS_DIFICIL = {'vida': 25, 'ataque': 6, 'defesa': 5, 'vel': 3, 'vel_ataque': 1,
                       'view_distance': 150, 'transpassavel': False}
    __DIST_PARA_ATAQUE = 8
    __CHANCE_DAMAGE_STOP_ATTACK = 0.2
    __FRAME_EXECUTAR_ATAQUE = 12

    def __init__(self, mapa: AbstractMapa, posicao=(0, 0)) -> None:
        super().__init__(mapa, MinotauroCinza.__SPRITE_PATH, posicao)

    @property
    def _SPRITE_PATH(self) -> str:
        return MinotauroCinza.__SPRITE_PATH

    @property
    def _STATS_DIFICIL(self) -> dict:
        return MinotauroCinza.__STATS_DIFICIL

    @property
    def _STATS_FACIL(self) -> dict:
        return MinotauroCinza.__STATS_FACIL

    @property
    def _STATS_MEDIO(self) -> dict:
        return MinotauroCinza.__STATS_MEDIO

    @property
    def _TAMANHO(self) -> tuple:
        return MinotauroCinza.__TAMANHO

    @property
    def _TAMANHO_IMAGEM(self) -> tuple:
        return MinotauroCinza.__TAMANHO_IMAGEM

    @property
    def _CHANCE_DAMAGE_STOP_ATTACK(self) -> float:
        return MinotauroCinza.__CHANCE_DAMAGE_STOP_ATTACK

    @property
    def _DIST_PARA_ATAQUE(self) -> tuple:
        return MinotauroCinza.__DIST_PARA_ATAQUE

    @property
    def _FRAME_EXECUTAR_ATAQUE(self) -> int:
        return MinotauroCinza.__FRAME_EXECUTAR_ATAQUE

    @property
    def hurt_sound_path(self) -> str:
        end = choice(MinotauroCinza.__HURT_SOUND_END_PATHS)
        path = MinotauroCinza.__HURT_SOUNDS_PATH_BASE + end
        return path

    @property
    def dying_sound_path(self) -> str:
        return MinotauroCinza.__DYING_SOUND_PATH
