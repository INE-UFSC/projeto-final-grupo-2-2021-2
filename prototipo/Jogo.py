import pygame
from TelaJogo import TelaJogo
from Jogador import Jogador
from Opcoes import Dificuldade, Opcoes
from Comandos import Comandos
from ControladorJogo import ControladorJogo


class Jogo:
    def __init__(self):
        self.__tela = TelaJogo()
        self.__comandos = Comandos()
        self.__jogador = None
        self.__controlador = None
        self.__opcoes = None

    def play(self):
        self.__tela.mostrar_fundo()
        self.__carregar_dados()

        loop = True
        while loop:

            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    loop = False
                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_RETURN:  # RETURN é o ENTER, dá inicio ao jogo no terreno 1
                        nova_fase = self.__controlador.proxima_fase()
                        nova_fase.start(self.__tela)

                pygame.display.update()

    def executar_comando(self):
        pass

    def mostrar_comando(self):
        pass

    def __escolher_dificuldade(self) -> Dificuldade:
        return Dificuldade.medio

    def __escolher_nome(self) -> str:
        return 'Tatakae'

    def __carregar_dados(self) -> None:
        dificuldade = self.__escolher_dificuldade()
        self.__opcoes = Opcoes(dificuldade)

        nome = self.__escolher_nome()
        self.__jogador = Jogador((0, 0), (10, 10), nome)

        self.__controlador = ControladorJogo(self.__jogador, self.__tela.tamanho, self.__opcoes)


pygame.init()


jogo = Jogo()
jogo.play()

pygame.quit()
