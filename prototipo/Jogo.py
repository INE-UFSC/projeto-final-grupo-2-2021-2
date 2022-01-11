import pygame
from Terreno1 import Terreno1
from Jogador import Jogador

class Jogo:
    def __init__(self, terreno, comandos, jogador, opcoes):
        self.__terreno = terreno
        self.__comandos = comandos
        self.__jogador = jogador
        self.__opcoes = opcoes

    def play(self):
        
        window = pygame.display.set_mode([1137, 640]) #cria a janela do jogo
        title = pygame.display.set_caption('The Binding Of Isaac') # nome da janela
        tela_start = pygame.image.load("imagens/start.png") # imagem da tela inicial
        window.blit(tela_start,(0,0)) # carrega a tela de start
        
        loop = True
        while loop:

            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    loop = False
                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_RETURN: #RETURN é o ENTER, dá inicio ao jogo no terreno 1
                        new_game = self.__terreno
                        new_game.rodar_jogo(window)

                pygame.display.update()
    def executar_comando(self):
        pass
    
    def mostrar_comando(self):
        pass

pygame.init()

terreno = Terreno1(0,0,0) #deixei 0 pois os atributos ainda não estão definidos

jogo = Jogo(terreno,0,0,0)
jogo.play()

pygame.quit()
