import pygame
from Views.TelaJogo import TelaJogo
from Personagens.Jogador.Jogador import Jogador
from Config.Opcoes import Opcoes
from Controller.ControladorFases import ControladorFases
from Abstractions.AbstractFase import AbstractFase


class Jogo:
    def __init__(self, opcoes: Opcoes):
        self.__tela = TelaJogo()
        self.__opcoes = opcoes
        self.__carregar_dados()
        self.__jogador = None
        self.__controlador = None
        self.__fase_atual = None

        self.__FPS = 40

    def start(self):
        clock = pygame.time.Clock()
        loop = True
        while loop:
            clock.tick(self.__FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.__rodar_fase()
                        loop = False

                pygame.display.update()

    def __wait(self):
        pass

    def __rodar_fase(self, fase: AbstractFase) -> None:
        self.__fase_atual = fase
        fase.start(self.__tela)
        pygame.display.update()

        clock = pygame.time.Clock()
        main_loop = True
        while main_loop:
            clock.tick(self.__FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main_loop = False

            self.__fase_atual.ciclo(self.__tela)

            if self.__fase_atual.is_player_dead():
                main_loop = False
                print('Você perdeu :/')

            if self.__fase_atual.has_ended():
                main_loop = False
                proxima_fase = self.__controlador.proxima_fase()
                if proxima_fase != None:
                    self.__rodar_fase(proxima_fase)
                else:
                    print('Você venceu :3')

            pygame.display.update()

    def __carregar_dados(self) -> None:
        self.__jogador = Jogador((0, 0), (50, 50), self.__opcoes.nome)
        self.__controlador = ControladorFases(self.__jogador)
