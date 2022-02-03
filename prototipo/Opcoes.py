from enum import Enum
import pygame
from Botao import Botao
from TelaJogo import TelaJogo


class Dificuldade(Enum):
    facil = 1
    medio = 2
    dificil = 3


class Opcoes():
    def __init__(self, dificuldade=Dificuldade, botoes_opcoes: list = [], botoes_dificuldade: list = []) -> None:
        self.__botoes_opcoes  = botoes_opcoes
        self.__botoes_dificuldade  = botoes_dificuldade
        self.__sprite_fundo = 'imagens/Menu_principal.png'
        self.__inicial = 0

        botao1 = Botao( (487, 300), (230, 55), 'imagens/dificuldade.png', "dificuldade")
        botao2 = Botao( (487, 360), (133, 55), 'imagens/voltar.png', "menu principal")
        botao_facil = Botao( (487, 300), (163, 55), 'imagens/facil.png', "facil")
        botao_medio = Botao( (487, 360), (163, 55), 'imagens/medio.png', "medio")
        botao_dificil = Botao( (487, 420), (163, 55), 'imagens/dificil.png', "dificil")
        botao_voltar = Botao( (487, 480), (163, 55), 'imagens/voltar.png', "voltar")
        self.__cursor = Botao((), (80, 37), 'imagens/seta.png', 'navegar')
        
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

    @property
    def inicial(self):
        return self.__inicial
    
    @inicial.setter
    def inicial(self, inicial):
        self.__inicial = inicial

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
        
        posicao_cursor = lista_posicoes[self.__inicial]
        x_cursor = posicao_cursor[0] - 100
        y_cursor = posicao_cursor[1]

        seta = pygame.image.load(self.cursor.imagem)
        tela.janela.blit(seta, (x_cursor,y_cursor))

        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:#subir
                                self.__inicial -= 1
                            elif event.key == pygame.K_DOWN:  #descer
                                self.__inicial += 1
                            elif event.key == pygame.K_RETURN:
                               for i in self.botoes_opcoes:
                                   if y_cursor == i.posicao[1]:
                                      return (i.acao)

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
        
        posicao_cursor = lista_posicoes[self.__inicial]
        x_cursor = posicao_cursor[0] - 100
        y_cursor = posicao_cursor[1]

        seta = pygame.image.load(self.cursor.imagem)
        tela.janela.blit(seta, (x_cursor,y_cursor))

        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:#subir
                                self.__inicial -= 1
                            elif event.key == pygame.K_DOWN:  #descer
                                self.__inicial += 1
                            elif event.key == pygame.K_RETURN:
                                ima = pygame.image.load("imagens/dificuldade_sel.png")
                                tela.janela.blit(ima, (487, 550))
                                for i in self.botoes_dificuldade:
                                   if y_cursor == i.posicao[1]:
                                       return (i.acao)
