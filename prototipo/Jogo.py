import pygame
from TelaJogo import TelaJogo
from Jogador import Jogador
from Opcoes import Dificuldade, Opcoes
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
            acao = menu.desenhar_cursor(self.__tela) 
            if acao != None:
                menu_loop = False
            pygame.display.update()
        self.executar_comando(acao)

    def opcoes(self):
        clock = pygame.time.Clock()
        opcoes_loop = True
        while opcoes_loop:
            clock.tick(self.__FPS)
            acao = self.__opcoes.desenhar_tela_opcoes(self.__tela)
            if acao != None:
                opcoes_loop = False            
            pygame.display.update()
        self.executar_comando(acao)

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

    def executar_comando(self, acao):
        if acao == "jogar":
            self.__carregar_dados()
            nova_fase = self.__controlador.proxima_fase()
            self.__rodar_fase(nova_fase)
        elif acao == "opcoes":
            self.opcoes()
        elif acao == "dificuldade":
            self.__escolher_dificuldade()
        elif acao == "menu principal" :
            self.menu_principal()

    def mostrar_comando(self):
        pass

    def __escolher_dificuldade(self) -> Dificuldade:
        clock = pygame.time.Clock()
        opcoes_loop = True
        while opcoes_loop:
            clock.tick(self.__FPS)
            dificuldade = self.__opcoes.desenhar_tela_dificuldade(self.__tela)
            
            if dificuldade != None:
                if dificuldade == "facil":
                    self.__dificuldade = Dificuldade.facil
                elif dificuldade == "medio":
                    self.dificuldade = Dificuldade.medio
                elif dificuldade == "dificil":
                    self.dificuldade = Dificuldade.dificil
                elif dificuldade == "voltar":
                    opcoes_loop = False
                    self.menu_principal()        
            pygame.display.update()

    def __escolher_nome(self) -> str:
        return 'Tatakae'

    def __carregar_dados(self) -> None:
        dificuldade = self.dificuldade
        self.__opcoes = Opcoes(dificuldade)

        nome = self.__escolher_nome()
        self.__jogador = Jogador((0, 0), (50, 50), nome)
        self.__opcoes = Opcoes(dificuldade)

        self.__controlador = ControladorJogo(self.__jogador, self.__tela.tamanho, self.__opcoes)
