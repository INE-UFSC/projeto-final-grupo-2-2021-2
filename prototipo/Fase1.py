import pygame
from Jogador import Jogador
from Opcoes import Opcoes
from TelaJogo import TelaJogo
from Terreno1 import Terreno1
from Inimigo1 import Inimigo1
from abstractions.AbstractFase import AbstractFase

QUANT_INIMIGOS = 5
INIMIGOS_POSICOES = [
    (600, 350),
    (380, 50),
    (150, 85),
    (500, 50),
    (40, 200)
]


class Fase1(AbstractFase):
    def __init__(self, jogador: Jogador, tamanho_tela: tuple, opcoes: Opcoes) -> None:
        self.__terreno = Terreno1(inimigos=[], itens=[], tamanho_tela=tamanho_tela)
        self.__dificuldade = opcoes.dificuldade
        self.__jogador = jogador

    def load(self) -> None:
        inimigos = []
        for x in range(QUANT_INIMIGOS):
            inimigos.append(Inimigo1(INIMIGOS_POSICOES[x], self.__dificuldade))
        self.__terreno.load_inimigos(inimigos)

    def has_ended(self) -> bool:
        return self.__terreno.has_ended()

    def start(self, tela: TelaJogo):
        self.__terreno.rodar_jogo(tela)
