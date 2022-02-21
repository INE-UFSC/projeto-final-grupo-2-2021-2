from enum import Enum


class ComandosEnum(Enum):
    SAIR = 1
    VOLTAR = 2
    LOAD_GAME = 3
    NEW_GAME = 4
    TELA_OPCOES = 5
    TELA_SAVES = 6
    TELA_NEW_GAME = 7
    TELA_MENU = 8
    TELA_JOGAR = 9
    SET_DIFICULDADE_FACIL = 10
    SET_DIFICULDADE_MEDIO = 11
    SET_DIFICULDADE_DIFICIL = 12
    TOGGLE_MUSICA = 13


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