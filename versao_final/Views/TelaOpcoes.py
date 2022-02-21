from typing import List
from Views.Components.Botao import Botao
from Enums.Enums import ComandosEnum
from Views.Components.Imagem import Imagem
from Abstractions.AbstractTela import AbstractTela
from Views.TelaJogo import TelaJogo
import pygame


class TelaOpcoes(AbstractTela):
    def __init__(self, comandos: dict) -> None:
        self.__comandos = comandos
        self.__FPS = 40
        self.__tela = TelaJogo()
        self.__botoes: List[Botao] = []
        self.__sprite_fundo = 'imagens/FundoFloresta.png'

        self.__criar_botoes()
        self.__criar_cursor()

    def run(self):
        clock = pygame.time.Clock()

        running = True
        while running:
            clock.tick(self.__FPS)
            self.__desenhar()

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
                        self.__executar_comando()

                pygame.display.update()

    def __desenhar(self) -> None:
        fundo = pygame.image.load(self.__sprite_fundo)
        fundo = pygame.transform.scale(fundo, self.__tela.tamanho)
        self.__tela.janela.blit(fundo, (0, 0))

        for botao in self.__botoes:
            tecla = pygame.image.load(botao.imagem)
            self.__tela.janela.blit(tecla, botao.posicao)

        self.__desenhar_cursor()

    def __desenhar_cursor(self):
        botao_selecionado = self.__botoes[self.__pos_cursor]
        x_cursor = botao_selecionado.posicao[0] - 100
        y_cursor = botao_selecionado.posicao[1]

        seta = pygame.image.load(self.__cursor.imagem)
        self.__tela.janela.blit(seta, (x_cursor, y_cursor))

    def __executar_comando(self):
        botao_escolhido = self.__botoes[self.__pos_cursor]
        botao_escolhido.execute()

    def __criar_botoes(self):
        funcSetFacil = self.__comandos[ComandosEnum.SET_DIFICULDADE_FACIL]
        funcSetMedio = self.__comandos[ComandosEnum.SET_DIFICULDADE_MEDIO]
        funcSetDificil = self.__comandos[ComandosEnum.SET_DIFICULDADE_DIFICIL]
        funcToggleMusica = self.__comandos[ComandosEnum.TOGGLE_MUSICA]
        funcVoltar = self.__comandos[ComandosEnum.VOLTAR]
        self.__botoes.append(Botao((487, 300), (230, 55), 'imagens/dificuldade.png', funcSetFacil))
        self.__botoes.append(Botao((587, 300), (230, 55), 'imagens/dificuldade.png', funcSetMedio))
        self.__botoes.append(
            Botao((687, 300), (230, 55), 'imagens/dificuldade.png', funcSetDificil))
        self.__botoes.append(
            Botao((657, 300), (230, 55), 'imagens/dificuldade.png', funcToggleMusica))
        self.__botoes.append(Botao((837, 360), (133, 55), 'imagens/voltar.png', funcVoltar))

    def __criar_cursor(self):
        self.__cursor = Imagem((), (80, 37), 'imagens/seta.png')
        self.__pos_cursor = 0

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
