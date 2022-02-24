import pygame
from Config.TelaJogo import TelaJogo


class TelaWait():
    def __init__(self):
        self.__tela = TelaJogo()
        self.__WAIT_FPS = 40
        self.__done = False

        self.__sprite_fundo = 'imagens/capa.png'

    def run(self):
        clock = pygame.time.Clock()

        menu_loop = True
        while menu_loop:
            clock.tick(self.__WAIT_FPS)
            self.__desenhar(self.__tela)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    menu_loop = False

                pygame.display.update()

    def __desenhar(self, tela: TelaJogo) -> None:
        fundo_menu = pygame.image.load(self.__sprite_fundo)
        tela.janela.blit(fundo_menu, (0, 0))

    def done(self):
        return self.__done
