from Enums.Enums import Dificuldade
import pygame
from Botao import Botao
from Enums.Enums import ComandosEnum
from TelaJogo import TelaJogo


class Opcoes():
    def __init__(self, dificuldade=Dificuldade, botoes_opcoes: list = [], botoes_dificuldade: list = []) -> None:
        self.__botoes_opcoes = botoes_opcoes
        self.__botoes_dificuldade = botoes_dificuldade
        self.__sprite_fundo = 'imagens/Menu_principal.png'
        self.__pos_cursor_opcoes = 0
        self.__pos_cursor_dificuldade = 0

        botao1 = Botao((487, 300), (230, 55), 'imagens/dificuldade.png',
                       ComandosEnum.VER_DIFICULDADE)
        botao2 = Botao((487, 360), (133, 55), 'imagens/voltar.png', ComandosEnum.VER_MENU)
        botao_facil = Botao((487, 300), (163, 55), 'imagens/facil.png', Dificuldade.facil)
        botao_medio = Botao((487, 360), (163, 55), 'imagens/medio.png', Dificuldade.medio)
        botao_dificil = Botao((487, 420), (163, 55), 'imagens/dificil.png', Dificuldade.dificil)
        botao_voltar = Botao((487, 480), (163, 55), 'imagens/voltar.png', ComandosEnum.VOLTAR)
        self.__cursor = Botao((), (80, 37), 'imagens/seta.png', ComandosEnum.NAVEGAR)

        self.__dificuldade_escolhida = Dificuldade.facil

        self.__botoes_opcoes.append(botao1)
        self.__botoes_opcoes.append(botao2)
        self.__botoes_dificuldade.append(botao_facil)
        self.__botoes_dificuldade.append(botao_medio)
        self.__botoes_dificuldade.append(botao_dificil)
        self.__botoes_dificuldade.append(botao_voltar)
        if isinstance(dificuldade, Dificuldade):
            self.__dificuldade = dificuldade
        else:
            self.__dificuldade = Dificuldade.facil

    @property
    def dificuldade(self) -> Dificuldade:
        return self.__dificuldade

    @property
    def dificuldade_escolhida(self) -> Dificuldade:
        return self.__dificuldade_escolhida

    @dificuldade.setter
    def dificuldade(self, dificuldade) -> None:
        if isinstance(dificuldade, Dificuldade):
            self.__dificuldade = dificuldade

    @property
    def sprite_fundo(self) -> str:
        return self.__sprite_fundo

    @sprite_fundo.setter
    def sprite_fundo(self, fundo) -> None:
        if type(fundo) == str:
            self.__sprite_fundo = fundo

    @property
    def botoes_opcoes(self) -> list:
        return self.__botoes_opcoes

    @botoes_opcoes.setter
    def botoes_opcoes(self, botoes_opcoes: list) -> None:
        if type(botoes_opcoes) == list:
            self.__botoes_opcoes = botoes_opcoes

    @property
    def botoes_dificuldade(self) -> list:
        return self.__botoes_dificuldade

    @botoes_dificuldade.setter
    def botoes_dificuldade(self, botoes_dificuldade: list) -> None:
        if type(botoes_dificuldade) == list:
            self.__botoes_dificuldade = botoes_dificuldade

    @property
    def cursor(self):
        return self.__cursor

    @cursor.setter
    def cursor(self, cursor) -> None:
        self.__cursor = cursor

    def desenhar_tela_opcoes(self, tela: TelaJogo) -> None:
        fundo_menu = pygame.image.load(self.sprite_fundo)
        tela.janela.blit(fundo_menu, (0, 0))
        lista_posicoes = []

        for i in self.__botoes_opcoes:
            imagem = i.imagem
            tecla = pygame.image.load(imagem)
            posicao = i.posicao
            tela.janela.blit(tecla, posicao)
            lista_posicoes.append(i.posicao)

        posicao_cursor = lista_posicoes[self.__pos_cursor_opcoes]
        x_cursor = posicao_cursor[0] - 100
        y_cursor = posicao_cursor[1]

        seta = pygame.image.load(self.cursor.imagem)
        tela.janela.blit(seta, (x_cursor, y_cursor))

    def get_comando_opcoes(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # subir
                    self.__subir_cursor_opcoes()
                elif event.key == pygame.K_DOWN:  # descer
                    self.__descer_cursor_opcoes()
                elif event.key == pygame.K_RETURN:
                    return self.__determinar_comando_opcoes()

    def desenhar_tela_dificuldade(self, tela: TelaJogo) -> None:
        fundo_menu = pygame.image.load(self.sprite_fundo)
        tela.janela.blit(fundo_menu, (0, 0))
        lista_posicoes = []

        for i in self.__botoes_dificuldade:
            imagem = i.imagem
            tecla = pygame.image.load(imagem)
            posicao = i.posicao
            tela.janela.blit(tecla, posicao)
            lista_posicoes.append(i.posicao)

        botao_escolhido = self.__botoes_dificuldade[self.__pos_cursor_dificuldade]
        x_cursor = botao_escolhido.posicao[0] - 100
        y_cursor = botao_escolhido.posicao[1]

        seta = pygame.image.load(self.cursor.imagem)
        tela.janela.blit(seta, (x_cursor, y_cursor))

    def get_comando_dificuldade(self, tela) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # subir
                    self.__subir_cursor_dificuldade()
                elif event.key == pygame.K_DOWN:  # descer
                    self.__descer_cursor_dificuldade()
                elif event.key == pygame.K_RETURN:
                    self.__determinar_dificuldade(tela)

                    if self.__deve_voltar():
                        return True

        return False

    def __subir_cursor_opcoes(self):
        if self.__pos_cursor_opcoes <= 0:
            self.__pos_cursor_opcoes = len(self.__botoes_opcoes) - 1
        else:
            self.__pos_cursor_opcoes -= 1

    def __descer_cursor_opcoes(self):
        if self.__pos_cursor_opcoes == len(self.__botoes_opcoes) - 1:
            self.__pos_cursor_opcoes = 0
        else:
            self.__pos_cursor_opcoes += 1

    def __subir_cursor_dificuldade(self):
        if self.__pos_cursor_dificuldade <= 0:
            self.__pos_cursor_dificuldade = len(self.__botoes_dificuldade) - 1
        else:
            self.__pos_cursor_dificuldade -= 1

    def __descer_cursor_dificuldade(self):
        if self.__pos_cursor_dificuldade == len(self.__botoes_dificuldade) - 1:
            self.__pos_cursor_dificuldade = 0
        else:
            self.__pos_cursor_dificuldade += 1

    def __determinar_dificuldade(self, tela):
        ima = pygame.image.load("imagens/dificuldade_sel.png")
        tela.janela.blit(ima, (487, 550))

        botao_selecionado = self.__botoes_dificuldade[self.__pos_cursor_dificuldade]
        if type(botao_selecionado.comando) == Dificuldade:
            self.__dificuldade_escolhida = botao_selecionado.comando

    def __deve_voltar(self) -> bool:
        botao_selecionado = self.__botoes_dificuldade[self.__pos_cursor_dificuldade]
        if botao_selecionado.comando == ComandosEnum.VOLTAR:
            return True
        else:
            return False

    def __determinar_comando_opcoes(self):
        botao_escolhido = self.__botoes_opcoes[self.__pos_cursor_opcoes]
        return botao_escolhido.comando
