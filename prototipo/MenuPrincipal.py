import pygame
from Botao import Botao
from TelaJogo import TelaJogo


class MenuPrincipal():
    def __init__(self, botoes: list = []):
        self.__botoes  = botoes
       
        self.__sprite_fundo = 'imagens/Menu_principal.png'
        botao1 = Botao( (487, 300), (163, 55), 'imagens/jogar.png', "jogar")
        botao2 = Botao( (487, 360), (163, 55), 'imagens/opcoes.png', "opcoes")
        botao3 = Botao( (487, 420), (163, 55), 'imagens/sair.png', "sair")
        self.__cursor = Botao((), (80, 37), 'imagens/seta.png', 'navegar')
        self.__botoes.append(botao1)
        self.__botoes.append(botao2)
        self.__botoes.append(botao3)
        self.__inicial = 0

    @property
    def botoes(self) -> list:
        return self.__botoes

    @botoes.setter
    def botoes(self, botoes: list) -> None:
        if type(botoes) == list:
            self.__botoes = botoes
    
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
    
    @property
    def sprite_fundo(self) -> str:
        return self.__sprite_fundo
    
    @sprite_fundo.setter
    def sprite_fundo(self, fundo) -> None:
        if type(fundo) == str:
            self.__sprite_fundo = fundo

    def desenhar(self, tela: TelaJogo) -> None:
        fundo_menu = pygame.image.load(self.sprite_fundo)
        tela.janela.blit(fundo_menu, (0, 0))
        for i in self.__botoes:
            imagem = i.imagem
            tecla = pygame.image.load(imagem)
            posicao = i.posicao
            tela.janela.blit(tecla, posicao)

    def desenhar_cursor(self, tela: TelaJogo) -> None:
        lista_posicoes = []
        
        for i in self.__botoes:
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
                               for i in self.botoes:
                                   if y_cursor == i.posicao[1]:
                                      return (i.acao)
                    pygame.display.update()