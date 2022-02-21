import pygame
import sys
from Config.Opcoes import Opcoes
from Enums.Enums import ComandosEnum, Dificuldade
from Config.TelaJogo import TelaJogo
from Views.Telas.TelaJogar import TelaJogar
from Views.Telas.TelaMenu import TelaMenuPrincipal
from Views.Telas.TelaOpcoes import TelaOpcoes
from Views.Telas.TelaWait import TelaWait
from Controller.Jogo import Jogo


class ControladorJogo():
    def __init__(self):
        self.__tela = TelaJogo()
        self.__MENU_FPS = 40

    def start(self):
        self.__tela.mostrar_fundo()

        self.__invoke_tela_wait()
        self.__invoke_menu()

    def __invoke_tela_wait(self):
        telaWait = TelaWait()
        telaWait.run()

    def __invoke_menu(self):
        telaMenu = TelaMenuPrincipal({
            ComandosEnum.TELA_JOGAR: self.__invoke_tela_jogar,
            ComandosEnum.TELA_OPCOES: self.__invoke_opcoes,
            ComandosEnum.SAIR: self.__end_game
        })
        telaMenu.run()

    def __invoke_opcoes(self):
        telaOptions = TelaOpcoes(
            {ComandosEnum.TELA_JOGAR: self.__invoke_game,
             ComandosEnum.SAIR: self.__end_game,
             ComandosEnum.VOLTAR: self.__invoke_menu,
             ComandosEnum.SET_DIFICULDADE_FACIL: self.__set_dificuldade_facil,
             ComandosEnum.SET_DIFICULDADE_MEDIO: self.__set_dificuldade_medio,
             ComandosEnum.SET_DIFICULDADE_DIFICIL: self.__set_dificuldade_dificil,
             ComandosEnum.TOGGLE_MUSICA: self.__toggle_musica

             })
        telaOptions.run()

    def __invoke_tela_jogar(self):
        telaJogar = TelaJogar({
            ComandosEnum.NEW_GAME: self.__invoke_new_game,
            ComandosEnum.LOAD_GAME: self.__invoke_saves,
            ComandosEnum.VOLTAR: self.__invoke_menu
        })
        telaJogar.run()

    def __end_game(self):
        pygame.quit()
        sys.exit()

    def __invoke_game(self):
        opcoes = Opcoes()
        self.__jogo = Jogo(opcoes)
        self.__jogo.start()

    def __invoke_saves(self):
        pass

    def __invoke_new_game(self):
        pass

    def __set_dificuldade_facil(self):
        options = Opcoes()
        options.dificuldade = Dificuldade.facil

    def __set_dificuldade_medio(self):
        options = Opcoes()
        options.dificuldade = Dificuldade.medio

    def __set_dificuldade_dificil(self):
        options = Opcoes()
        options.dificuldade = Dificuldade.dificil

    def __toggle_musica(self):
        opcoes = Opcoes()
        opcoes.tocar_musica = not opcoes.tocar_musica