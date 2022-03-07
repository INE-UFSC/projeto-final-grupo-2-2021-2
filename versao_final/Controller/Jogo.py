import pygame
from Config.TelaJogo import TelaJogo
from Personagens.Jogador.Jogador import Jogador
from Config.Opcoes import Opcoes
from Controller.ControladorFases import ControladorFases
from Abstractions.AbstractFase import AbstractFase


class Jogo:
    def __init__(self):
        pygame.init()  # Temporariamente enquanto não mexo nas telas
        self.__tela = TelaJogo()
        self.__opcoes = Opcoes()
        self.__jogador = None
        self.__controlador = None
        self.__fase_atual = None

        self.__carregar_dados()
        self.__FPS = 40

    def start(self):
        primeira_fase = self.__controlador.proxima_fase()
        self.__rodar_fase(primeira_fase)

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

            if self.__fase_atual.player_has_lost():
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
        self.__jogador = Jogador((0, 0), self.__opcoes.nome)
        self.__controlador = ControladorFases(self.__jogador)
