import pygame
from abstractions.AbstractTerreno import AbstractTerreno


class Terreno3(AbstractTerreno):

    def __init__(self, personagens, item, hitbox):

        self.__personagens = personagens
        self.__item = item
        self.__hitbox = hitbox

    def rodar_jogo(self, window):
        pass

    def dropar_item():
        pass

    def remover_inimigo():
        pass

    def validar_movimento():
        pass

    def iniciar_rodada():
        pass