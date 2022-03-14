import pygame
from Config.TelaJogo import TelaJogo
from Personagens.Jogador import Jogador
from Config.Opcoes import Opcoes
from Controllers.ControladorFases import ControladorFases
from Fases.AbstractFase import AbstractFase
from Sounds.MusicHandler import MusicHandler
from Views.Telas.TelaPause import TelaPause
from Config.Enums import ComandosEnum


class Jogo:
    def __init__(self):
        pygame.init()  # Temporariamente enquanto não mexo nas telas
        self.__music = MusicHandler()
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
        self.__tela_pause = self.__criar_tela_pause()
        fase.start(self.__tela)
        pygame.display.update()

        clock = pygame.time.Clock()
        self.__paused = False
        self.__GAME_LOOP = True
        while self.__GAME_LOOP:
            clock.tick(self.__FPS)
            eventos = pygame.event.get()

            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.__GAME_LOOP = False

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.__paused = not self.__paused

            self.__fase_atual.desenhar(self.__tela)
            self.__music.update()
            if self.__paused:
                self.__tela_pause.desenhar()
                self.__tela_pause.run(eventos)
            else:
                self.__fase_atual.run()
                if self.__fase_atual.player_has_lost():
                    self.__GAME_LOOP = False
                    print('Você perdeu :/')

                if self.__fase_atual.player_has_won():
                    self.__GAME_LOOP = False
                    proxima_fase = self.__controlador.proxima_fase()
                    if proxima_fase != None:
                        self.__rodar_fase(proxima_fase)
                    else:
                        print('Você venceu :3')

            pygame.display.update()

    def __carregar_dados(self) -> None:
        self.__jogador = Jogador((0, 0), self.__opcoes.nome)
        self.__controlador = ControladorFases(self.__jogador)

    def __criar_tela_pause(self, *args) -> TelaPause:
        return TelaPause({
            ComandosEnum.TELA_JOGAR: self.__voltar_jogo,
            ComandosEnum.TELA_OPCOES: self.__opcoes_pause,
            ComandosEnum.TELA_MENU: self.__menu_principal
        })

    def __voltar_jogo(self, *args):
        self.__paused = False

    def __opcoes_pause(self, *args):
        print('aoba')

    def __menu_principal(self, *args):
        self.__GAME_LOOP = False
