import pygame
from Controllers.ControladorJogo import ControladorJogo
from Views.ControladorTelas import ControladorTelas
from Controllers.Jogo import Jogo

jogo = ControladorTelas()
jogo.start()
pygame.quit()
