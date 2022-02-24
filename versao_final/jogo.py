import pygame
from Controller.ControladorJogo import ControladorJogo
from Controller.Jogo import Jogo

pygame.init()
jogo = Jogo()
jogo.start()
pygame.quit()
