import pygame
from abstractions.AbstractTerreno import AbstractTerreno


class Terreno2(AbstractTerreno):

    def __init__(self, personagens, item, hitbox):

        self.__personagens = personagens
        self.__item = item
        self.__hitbox = hitbox

    def rodar_jogo(self, window):

        mapa1 = pygame.image.load("imagens/terreno1.png")
        window.blit(mapa1, (0, 0))

    def dropar_item():
        pass

    def remover_inimigo():
        pass

    def validar_movimento():
        pass

    def iniciar_rodada():
        pass
