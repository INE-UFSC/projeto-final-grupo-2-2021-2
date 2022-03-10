import pygame
import sys
from Config.Opcoes import Opcoes
from Config.Enums import ComandosEnum
from Config.TelaJogo import TelaJogo
from Views.Telas.TelaJogar import TelaJogar
from Views.Telas.TelaMenu import TelaMenuPrincipal
from Views.Telas.TelaNew import TelaNewGame
from Views.Telas.TelaOpcoes import TelaOpcoes
from Controllers.Jogo import Jogo


class ControladorJogo():
    def __init__(self):
        pygame.init()
        self.__tela = TelaJogo()
        self.__MENU_FPS = 40

    def start(self):
        self.__tela.mostrar_fundo()

        self.__invoke_menu()

    def __invoke_menu(self, *args, **kwargs):
        telaMenu = TelaMenuPrincipal({
            ComandosEnum.TELA_JOGAR: self.__invoke_tela_jogar,
            ComandosEnum.TELA_OPCOES: self.__invoke_opcoes,
            ComandosEnum.SAIR: self.__end_game
        })
        telaMenu.run()

    def __invoke_opcoes(self, *args, **kwargs):
        telaOptions = TelaOpcoes(
            {ComandosEnum.TELA_JOGAR: self.__invoke_game,
             ComandosEnum.SAIR: self.__end_game,
             ComandosEnum.VOLTAR: self.__invoke_menu,
             ComandosEnum.SET_DIFICULDADE: self.__set_dificuldade,
             ComandosEnum.TOGGLE_MUSICA: self.__toggle_musica

             })
        telaOptions.run()

    def __invoke_tela_jogar(self, *args, **kwargs):
        telaJogar = TelaJogar({
            ComandosEnum.NEW_GAME: self.__invoke_new_game,
            ComandosEnum.LOAD_GAME: self.__invoke_saves,
            ComandosEnum.VOLTAR: self.__invoke_menu
        })
        telaJogar.run()

    def __end_game(self, *args, **kwargs):
        pygame.quit()
        sys.exit()

    def __invoke_game(self, *args, **kwargs):
        self.__jogo = Jogo()
        self.__jogo.start()
        self.__invoke_menu()

    def __invoke_saves(self, *args, **kwargs):
        pass

    def __invoke_new_game(self, *args, **kwargs):
        telaNew = TelaNewGame({
            ComandosEnum.NEW_GAME: self.__invoke_game,
            ComandosEnum.VOLTAR: self.__invoke_tela_jogar
        })
        telaNew.run()

    def __set_dificuldade(self, *args, **kwargs):
        dificuldade = args[0]
        options = Opcoes()
        options.dificuldade = dificuldade

    def __toggle_musica(self, *args, **kwargs):
        opcoes = Opcoes()
        opcoes.tocar_musica = not opcoes.tocar_musica
