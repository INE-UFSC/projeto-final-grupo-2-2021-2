from typing import List
from Utils.Folder import import_single_sprite
from Utils.Hitbox import Hitbox
from Views.Components.Botao import Botao
from Views.Components.Imagem import Imagem
from Views.Components.Text import Text
from Config.Enums import ComandosEnum
from Views.Telas.AbstractTela import AbstractTela
from Config.TelaJogo import TelaJogo
from Config.Opcoes import Opcoes
import pygame


X_OFFSET = 75
POS_BOTOES = [(430, 320), (430, 367), (800, 200)]
TAM_BOTAO = (150, 50)
TAM_TEXTO = (400, 100)


class TelaPause(AbstractTela):
    __POS = (575, 375)
    __SIZE = (550, 450)
    __FUNDO_PATH = 'Assets/Telas/FundoPause.png'
    __SOM_PATH = 'Assets/Telas/som.png'
    __MUTADO_PATH = 'Assets/Telas/mutado.png'
    __SPRITE_SOM = None
    __SPRITE_MUTADO = None
    __SIZE_SOM = (60, 60)
    __POS_SOM = (800, 200)

    def __init__(self, comandos: dict):
        self.__hitbox = Hitbox(TelaPause.__POS, TelaPause.__SIZE)
        self.__opcoes = Opcoes()

        self.__load_sprites()

        self.__comandos = comandos
        self.__tela = TelaJogo()
        self.__botoes: List[Botao] = []
        self.__textos: List[Text] = []
        self.__cursor: Imagem = None
        self.__criar_botoes()
        self.__criar_cursor()

    def __load_sprites(self) -> None:
        image_som = import_single_sprite(TelaPause.__SOM_PATH, TelaPause.__SIZE_SOM)
        image_mutado = import_single_sprite(TelaPause.__MUTADO_PATH, TelaPause.__SIZE_SOM)
        TelaPause.__SPRITE_SOM = image_som
        TelaPause.__SPRITE_MUTADO = image_mutado

        self.__image = import_single_sprite(TelaPause.__FUNDO_PATH, TelaPause.__SIZE)
        self.__rect = self.__image.get_rect(center=self.__hitbox.posicao)

    def desenhar(self):
        self.__tela.janela.blit(self.__image, self.__rect)
        self.__desenhar_elementos()
        self.__desenhar_caixa_som()

    def run(self, eventos: List[pygame.event.Event]) -> None:
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:  # Subir
                    self.__subir_cursor()
                elif evento.key == pygame.K_DOWN:  # Descer
                    self.__descer_cursor()
                elif evento.key == pygame.K_RETURN:  # Enter
                    self.__executar_comando()

    def __desenhar_caixa_som(self) -> None:
        som = True if self.__opcoes.tocar_musica else False

        if som:
            image = TelaPause.__SPRITE_SOM
        else:
            image = TelaPause.__SPRITE_MUTADO

        rect = image.get_rect(center=TelaPause.__POS_SOM)
        self.__tela.janela.blit(image, rect)

    def __desenhar_elementos(self):
        botao_atual = self.__botoes[self.__pos_cursor]
        posicao_y = botao_atual.hitbox.y
        posicao_x = botao_atual.hitbox.x - X_OFFSET

        nova_posicao = (posicao_x, posicao_y)

        self.__cursor.hitbox.posicao = nova_posicao
        self.__cursor.desenhar(self.__tela)

    def __executar_comando(self):
        botao_selecionado = self.__botoes[self.__pos_cursor]
        botao_selecionado.execute()

    def __criar_botoes(self):
        funcContinuar = self.__comandos[ComandosEnum.TELA_JOGAR]
        funcSair = self.__comandos[ComandosEnum.TELA_MENU]

        self.__botoes.append(Botao(POS_BOTOES[0], TAM_BOTAO, 'Continuar', funcContinuar))
        self.__botoes.append(Botao(POS_BOTOES[1], TAM_BOTAO, 'Sair', funcSair))
        self.__botoes.append(Botao(POS_BOTOES[2], TAM_BOTAO, 'Musica', self.__toggle_musica))

    def __toggle_musica(self, *args) -> None:
        self.__opcoes.tocar_musica = not self.__opcoes.tocar_musica

    def __criar_cursor(self):
        self.__cursor = Imagem(POS_BOTOES[0], (110, 32), 'Assets/Telas/seta.png')
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
