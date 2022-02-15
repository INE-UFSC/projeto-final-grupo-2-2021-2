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


class Direction(Enum):
    ESQUERDA_BAIXO = 1
    ESQUERDA_MEIO = 2
    ESQUERDA_CIMA = 3
    MEIO_CIMA = 4
    MEIO_BAIXO = 5
    DIREITA_BAIXO = 6
    DIREITA_MEIO = 7
    DIREITA_CIMA = 8
