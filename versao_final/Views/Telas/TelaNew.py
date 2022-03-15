from typing import List
from Views.Components.Botao import Botao
from Views.Components.Imagem import Imagem
from Views.Components.Text import Text
from Config.Enums import ComandosEnum
from Views.Telas.AbstractTela import AbstractTela
from Config.TelaJogo import TelaJogo
import pygame

X_OFFSET = 100
POS_TEXTO = [(550, 50)]
POS_BOTOES = [(550, 300), (550, 370), (550, 440)]
TAM_BOTAO = (150, 50)
TAM_TEXTO = (400, 100)


class TelaNewGame(AbstractTela):
    def __init__(self, comandos: dict):
        self.__comandos = comandos
        self.__tela = TelaJogo()
        self.__sprite_fundo = 'Assets/Telas/FundoFloresta.png'

        self.__MENU_FPS = 40
        self.__save_name = 'Save1'

        self.__botoes: List[Botao] = []
        self.__textos: List[Text] = []
        self.__cursor: Imagem = None
        self.__criar_botoes()
        self.__criar_textos()
        self.__criar_cursor()

    def run(self):
        clock = pygame.time.Clock()

        menu_loop = True
        while menu_loop:
            clock.tick(self.__MENU_FPS)
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

        self.__desenhar_elementos()

    def __update(self) -> None:
        botao_save = self.__botoes[0]
        botao_save.mudar_texto(f'Save: {self.__save_name}')

    def __editar_save(self):
        botao_save = self.__botoes[0]
        nome_escolhido = botao_save.texto[4:]
        self.__save_name = nome_escolhido

    def __desenhar_elementos(self):
        for botao in self.__botoes:
            botao.desenhar(self.__tela)

        for texto in self.__textos:
            texto.desenhar(self.__tela)

        botao_atual = self.__botoes[self.__pos_cursor]
        posicao_y = botao_atual.hitbox.y
        posicao_x = botao_atual.hitbox.x - X_OFFSET

        nova_posicao = (posicao_x, posicao_y)

        self.__cursor.hitbox.posicao = nova_posicao
        self.__cursor.desenhar(self.__tela)

    def __executar_comando(self):
        botao_selecionado = self.__botoes[self.__pos_cursor]
        botao_selecionado.execute()

    def __toggle_botao_save(self):
        pass

    def __criar_textos(self):
        branco = (255, 255, 255)
        self.__textos.append(Text(POS_TEXTO[0], TAM_TEXTO, 'The Binding of Isaac', 60, branco))

    def __criar_botoes(self):
        funcJogar = self.__comandos[ComandosEnum.NEW_GAME]
        funcVoltar = self.__comandos[ComandosEnum.VOLTAR]

        self.__botoes.append(Botao(POS_BOTOES[0], TAM_BOTAO, 'Nome: Save1', self.__editar_save))
        self.__botoes.append(Botao(POS_BOTOES[1], TAM_BOTAO, 'Play', funcJogar, self.__save_name))
        self.__botoes.append(Botao(POS_BOTOES[2], TAM_BOTAO, 'Voltar', funcVoltar))

    def __criar_cursor(self):
        self.__cursor = Imagem(POS_BOTOES[0], (50, 40), 'Assets/Telas/seta.png')
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
