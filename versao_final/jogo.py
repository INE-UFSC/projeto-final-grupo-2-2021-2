from tkinter import Menu
import pygame
from Controller.ControladorJogo import ControladorJogo

pygame.init()
jogo = ControladorJogo()
jogo.start()
pygame.quit()
