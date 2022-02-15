import pygame
from Views.Botao import Botao
from Enums.Enums import ComandosEnum
from Views.TelaJogo import TelaJogo


class MenuPrincipal():
    def __init__(self, botoes: list = []):
        self.__botoes = botoes

        self.__sprite_fundo = 'imagens/Menu_principal.png'
        botao1 = Botao((487, 300), (163, 55), 'imagens/jogar.png', ComandosEnum.JOGAR)
        botao2 = Botao((487, 360), (163, 55), 'imagens/opcoes.png', ComandosEnum.VER_OPCOES)
        botao3 = Botao((487, 420), (163, 55), 'imagens/sair.png', ComandosEnum.SAIR)
        self.__cursor = Botao((), (80, 37), 'imagens/seta.png', ComandosEnum.NAVEGAR)
        self.__botoes.append(botao1)
        self.__botoes.append(botao2)
        self.__botoes.append(botao3)
        self.__pos_cursor = 0

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
    def pos_cursor(self):
        return self.__pos_cursor

    @pos_cursor.setter
    def pos_cursor(self, pos_cursor):
        self.__pos_cursor = pos_cursor

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

        for botao in self.__botoes:
            imagem = botao.imagem
            tecla = pygame.image.load(imagem)
            posicao = botao.posicao
            tela.janela.blit(tecla, posicao)

        self.__desenhar_cursor(tela)

    def __desenhar_cursor(self, tela: TelaJogo) -> None:
        botao_selecionado = self.__botoes[self.__pos_cursor]
        x_cursor = botao_selecionado.posicao[0] - 100
        y_cursor = botao_selecionado.posicao[1]

        seta = pygame.image.load(self.cursor.imagem)
        tela.janela.blit(seta, (x_cursor, y_cursor))

    def get_comando(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # Subir
                    self.__subir_cursor()
                elif event.key == pygame.K_DOWN:  # Descer
                    self.__descer_cursor()
                elif event.key == pygame.K_RETURN:  # Enter
                    return self.__determinar_comando()

            pygame.display.update()

    def __subir_cursor(self):
        if self.__pos_cursor <= 0:
            self.__pos_cursor = len(self.__botoes) - 1
        else:
            self.__pos_cursor -= 1

    def __descer_cursor(self):
        if self.__pos_cursor == len(self.__botoes) - 1:
            self.__pos_cursor = 0
        else:
            self.__pos_cursor += 1

    def __determinar_comando(self):
        botao_selecionado = self.__botoes[self.__pos_cursor]
        return botao_selecionado.comando
