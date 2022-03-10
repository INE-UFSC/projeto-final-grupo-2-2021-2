import pygame
from Config.TelaJogo import TelaJogo
from Personagens.Jogador.Jogador import Jogador
from Config.Opcoes import Opcoes
from Controller.ControladorFases import ControladorFases
from Abstractions.AbstractFase import AbstractFase
from Views.Telas.TelaPause import TelaPause
from Enums.Enums import ComandosEnum


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
        self.__menuprincipal = False
        while main_loop:
            clock.tick(self.__FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main_loop = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.tela_pause()

            if self.__menuprincipal:  # volta para o menu principal, quando o jogo é rodado pelo ControladorJogo
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

    def tela_pause(self, *args) -> None:
        telaPause = TelaPause({
            ComandosEnum.TELA_JOGAR: self.__voltar_jogo,
            ComandosEnum.TELA_OPCOES: self.__opcoes_pause,
            ComandosEnum.TELA_MENU: self.__menu_principal
        })
        telaPause.run()

    def __voltar_jogo(self, *args):
        pass

    def __opcoes_pause(self, *args):
        pass

    def __menu_principal(self, *args):
        voltar = args[0][0]
        self.__menuprincipal = voltar
