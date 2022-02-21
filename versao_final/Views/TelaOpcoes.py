from typing import List
from Config.Opcoes import Opcoes
from Views.Components.Botao import Botao
from Enums.Enums import ComandosEnum
from Views.Components.Imagem import Imagem
from Abstractions.AbstractTela import AbstractTela
from Views.Components.Texto import Texto
from Views.TelaJogo import TelaJogo
import pygame

X_OFFSET = 100
POS_TITULO = (550, 50)
POS_DIFICULDADE = (250, 200)
POS_BOTOES = [(250, 250), (250, 320), (250, 390), (700, 250), (700, 390)]
TAM_BOTAO = (150, 50)
TAM_TITULO = (400, 100)
TAM_DIFICULDADE = (100, 100)


class TelaOpcoes(AbstractTela):
    def __init__(self, comandos: dict) -> None:
        self.__comandos = comandos
        self.__FPS = 40
        self.__tela = TelaJogo()
        self.__botoes: List[Botao] = []
        self.__sprite_fundo = 'imagens/FundoFloresta.png'
        self.__opcoes = Opcoes()

        self.__botoes: List[Botao] = []
        self.__textos: List[Texto] = []
        self.__cursor: Imagem = None
        self.__criar_botoes()
        self.__criar_cursor()
        self.__criar_textos()

    def run(self):
        clock = pygame.time.Clock()

        running = True
        while running:
            clock.tick(self.__FPS)
            self.__update()
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
                    elif event.key == pygame.K_RIGHT:  # Direita
                        self.__direita_cursor()
                    elif event.key == pygame.K_LEFT:  # Esquerda
                        self.__esquerda_cursor()
                    elif event.key == pygame.K_RETURN:  # Enter
                        self.__executar_comando()

                pygame.display.update()

    def __desenhar(self) -> None:
        fundo = pygame.image.load(self.__sprite_fundo)
        fundo = pygame.transform.scale(fundo, self.__tela.tamanho)
        self.__tela.janela.blit(fundo, (0, 0))

        self.__desenhar_elementos()

    def __update(self):
        botao_musica = self.__botoes[3]
        status = 'On' if self.__opcoes.tocar_musica else 'Off'
        botao_musica.mudar_texto(f'Música: {status}')

    def __desenhar_elementos(self) -> None:
        for botao in self.__botoes:
            botao.desenhar(self.__tela)

        for texto in self.__textos:
            texto.desenhar(self.__tela)

        botao_selecionado = self.__botoes[self.__pos_cursor]
        pos_x = botao_selecionado.hitbox.posicao[0] - X_OFFSET
        pos_y = botao_selecionado.hitbox.posicao[1]
        nova_posicao = (pos_x, pos_y)

        self.__cursor.hitbox.posicao = nova_posicao
        self.__cursor.desenhar(self.__tela)

    def __executar_comando(self):
        botao_escolhido = self.__botoes[self.__pos_cursor]
        botao_escolhido.execute()

    def __criar_botoes(self):
        funcSetFacil = self.__comandos[ComandosEnum.SET_DIFICULDADE_FACIL]
        funcSetMedio = self.__comandos[ComandosEnum.SET_DIFICULDADE_MEDIO]
        funcSetDificil = self.__comandos[ComandosEnum.SET_DIFICULDADE_DIFICIL]
        funcToggleMusica = self.__comandos[ComandosEnum.TOGGLE_MUSICA]
        funcVoltar = self.__comandos[ComandosEnum.VOLTAR]

        status = 'On' if self.__opcoes.tocar_musica else 'Off'

        self.__botoes.append(Botao(POS_BOTOES[0], TAM_BOTAO, 'Fácil', funcSetFacil))
        self.__botoes.append(Botao(POS_BOTOES[1], TAM_BOTAO, 'Médio', funcSetMedio))
        self.__botoes.append(Botao(POS_BOTOES[2], TAM_BOTAO, 'Difícil', funcSetDificil))
        self.__botoes.append(Botao(POS_BOTOES[3], TAM_BOTAO, f'Música: {status}', funcToggleMusica))
        self.__botoes.append(Botao(POS_BOTOES[4], TAM_BOTAO, 'Voltar', funcVoltar))

    def __criar_textos(self):
        branco = (255, 255, 255)
        preto = (0, 0, 0)
        self.__textos.append(Texto(POS_TITULO, TAM_TITULO, 'The Binding of Isaac', 60, branco))
        self.__textos.append(Texto(POS_DIFICULDADE, TAM_DIFICULDADE, 'Dificuldade: ', 30, preto))

    def __criar_cursor(self):
        self.__cursor = Imagem(POS_BOTOES[0], (50, 40), 'imagens/seta.png')
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

    def __direita_cursor(self):
        pass

    def __esquerda_cursor(self):
        pass
