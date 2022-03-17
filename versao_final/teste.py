import pygame
from Sounds.MusicHandler import MusicHandler
from Config.TelaJogo import TelaJogo
pygame.init()
tela = TelaJogo()
tela.mostrar_fundo()

music = MusicHandler()

path = 'Sounds/musics/lose/lose_music_10.mp3'
music.play_music_once(path)
