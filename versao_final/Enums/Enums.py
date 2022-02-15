from enum import Enum


class ComandosEnum(Enum):
    SAIR = 1
    VOLTAR = 2
    JOGAR = 3
    VER_DIFICULDADE = 4
    VER_OPCOES = 5
    VER_MENU = 6
    NAVEGAR = 7


class Dificuldade(Enum):
    facil = 1
    medio = 2
    dificil = 3
