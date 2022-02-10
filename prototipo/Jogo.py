import pygame
from Enums.Enums import ComandosEnum, Dificuldade
from TelaJogo import TelaJogo
from Jogador import Jogador
from Opcoes import Opcoes
from Comandos import Comandos
from ControladorJogo import ControladorJogo
from abstractions.AbstractFase import AbstractFase
from MenuPrincipal import MenuPrincipal


class Jogo:
    def __init__(self):
        self.__tela = TelaJogo()
        self.__comandos = Comandos()
        self.__jogador = None
        self.__controlador = None
        self.__opcoes = Opcoes()
        self.__fase_atual = None
        self.__dificuldade = None

        self.__FPS = 40

    @property
    def dificuldade(self) -> Dificuldade:
        return self.__dificuldade

    @dificuldade.setter
    def dificuldade(self, dificuldade) -> None:
        if isinstance(dificuldade, Dificuldade):
            self.__dificuldade = dificuldade

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
                    if event.key == pygame.K_RETURN:
                        self.menu_principal()
                        loop = False

                pygame.display.update()

    def menu_principal(self):
        menu = MenuPrincipal()
        clock = pygame.time.Clock()
        menu_loop = True

        while menu_loop:
            clock.tick(self.__FPS)
            menu.desenhar(self.__tela)

            comando = menu.get_comando()
            if comando != None:
                menu_loop = False
            pygame.display.update()

        self.executar_comando(comando)

    def __menu_opcoes(self):
        clock = pygame.time.Clock()
        opcoes_loop = True
        while opcoes_loop:
            clock.tick(self.__FPS)
            self.__opcoes.desenhar_tela_opcoes(self.__tela)
            comando = self.__opcoes.get_comando_opcoes()

            if comando != None:
                opcoes_loop = False
            pygame.display.update()
        self.executar_comando(comando)

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
            if self.__jogador.verificar_ataque(keys_pressed):
                self.__fase_atual.terreno.executar_ataque(self.__tela, self.__jogador)

            if self.__fase_atual.has_ended():
                main_loop = False
                proxima_fase = self.__controlador.proxima_fase()
                if proxima_fase != None:
                    print('Proxima fase')
                    self.__rodar_fase(proxima_fase)
                else:
                    print('Você venceu :3')

            pygame.display.update()

    def executar_comando(self, comando: ComandosEnum):
        if type(comando) != ComandosEnum:
            return

        if comando == ComandosEnum.JOGAR:
            self.__carregar_dados()
            nova_fase = self.__controlador.proxima_fase()
            self.__rodar_fase(nova_fase)

        elif comando == ComandosEnum.VER_OPCOES:
            self.__menu_opcoes()

        elif comando == ComandosEnum.VER_DIFICULDADE:
            self.__escolher_dificuldade()

        elif comando == ComandosEnum.VER_MENU:
            self.menu_principal()

    def mostrar_comando(self):
        pass

    def __escolher_dificuldade(self) -> Dificuldade:
        clock = pygame.time.Clock()
        opcoes_loop = True
        while opcoes_loop:
            clock.tick(self.__FPS)
            self.__opcoes.desenhar_tela_dificuldade(self.__tela)
            voltar = self.__opcoes.get_comando_dificuldade(self.__tela)

            pygame.display.update()

            if voltar:
                self.__dificuldade = self.__opcoes.dificuldade_escolhida
                opcoes_loop = False
                self.__menu_opcoes()

    def __escolher_nome(self) -> str:
        return 'Tatakae'

    def __carregar_dados(self) -> None:
        nome = self.__escolher_nome()
        self.__jogador = Jogador((0, 0), (50, 50), nome)
        self.__opcoes = Opcoes(self.dificuldade)

        self.__controlador = ControladorJogo(self.__jogador, self.__tela.tamanho, self.__opcoes)
