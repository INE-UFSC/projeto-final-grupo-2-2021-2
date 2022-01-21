import pygame
from TelaJogo import TelaJogo
from Jogador import Jogador
from Opcoes import Dificuldade, Opcoes
from Comandos import Comandos
from ControladorJogo import ControladorJogo
from abstractions.AbstractFase import AbstractFase


class Jogo:
    def __init__(self):
        self.__tela = TelaJogo()
        self.__comandos = Comandos()
        self.__jogador = None
        self.__controlador = None
        self.__opcoes = None
        self.__fase_atual = None

        self.__FPS = 40

    def start(self):
        self.__tela.mostrar_fundo()
        self.__carregar_dados()

        clock = pygame.time.Clock()
        loop = True
        while loop:
            clock.tick(self.__FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # RETURN é o ENTER, dá inicio ao jogo no terreno 1
                        nova_fase = self.__controlador.proxima_fase()
                        self.__rodar_fase(nova_fase)
                        loop = False

                pygame.display.update()

    def __rodar_fase(self, fase: AbstractFase) -> None:
        self.__fase_atual = fase
        fase.start(self.__tela)
        pygame.display.update()

        clock = pygame.time.Clock()
        main_loop = True
        while main_loop:
            clock.tick(self.__FPS)
            keys_pressed = pygame.key.get_pressed()
            self.__jogador.lidar_inputs(keys_pressed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main_loop = False

            self.__fase_atual.ciclo(self.__tela)
            pygame.display.update()

    def executar_comando(self):
        pass

    def mostrar_comando(self):
        pass

    def __escolher_dificuldade(self) -> Dificuldade:
        return Dificuldade.dificil

    def __escolher_nome(self) -> str:
        return 'Tatakae'

    def __carregar_dados(self) -> None:
        dificuldade = self.__escolher_dificuldade()
        self.__opcoes = Opcoes(dificuldade)

        nome = self.__escolher_nome()
        self.__jogador = Jogador((0, 0), (50, 50), nome)

        self.__controlador = ControladorJogo(self.__jogador, self.__tela.tamanho, self.__opcoes)