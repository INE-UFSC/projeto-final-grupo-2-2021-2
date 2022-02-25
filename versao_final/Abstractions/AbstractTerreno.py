from abc import ABC, abstractmethod
from Utils.Hitbox import Hitbox
from Obstaculos.Buraco import Buraco
from Obstaculos.Parede import Parede
from Personagens.Jogador.Jogador import Jogador
from Config.Opcoes import Opcoes
from Config.TelaJogo import TelaJogo
from Abstractions.AbstractPersonagem import AbstractPersonagem
from Utils.Movement import gerar_equação_vetorial_reta
from Itens.PocaoDefesa import PocaoDefesa
from Itens.PocaoMedia import PocaoMedia
from Itens.PocaoPequena import PocaoPequena
from Itens.PocaoInvencivel import PocaoInvencivel
import pygame
import random


class AbstractTerreno(ABC):
    def __init__(self, inimigos: list, itens: list, jogador, sprite_path: str):
        self.__inimigos = inimigos
        self.__obstaculos = []
        self.__itens = itens
        self.__matrix = []

        self.__opcoes = Opcoes()
        self.__hitbox = Hitbox(posicao=(0, 0), tamanho=self.__opcoes.TAMANHO_TELA)
        self.__jogador = jogador
        self.__sprite_path = sprite_path

        self.__itens_tela = []
        pocao_defesa = PocaoDefesa()
        pocao_media = PocaoMedia()
        pocao_invencivel = PocaoInvencivel()
        pocao_pequena = PocaoPequena()
        self.__itens.append(pocao_defesa)
        self.__itens.append(pocao_media)
        self.__itens.append(pocao_invencivel)
        self.__itens.append(pocao_pequena)

    def _setup_mapa(self, matriz_terreno: list) -> None:
        self.__matrix = matriz_terreno

        for index_row, row in enumerate(matriz_terreno):
            for index_column, cell in enumerate(row):
                if cell == 'B':  # Buraco
                    self.__obstaculos.append(Buraco((index_column, index_row)))
                elif cell == 'P':  # Parede
                    self.__obstaculos.append(Parede((index_column, index_row)))
                elif cell == 'J':  # Jogador
                    nova_posicao = (index_column * 32, index_row * 32)
                    self.__jogador.hitbox.posicao = nova_posicao

    def iniciar_rodada(self, tela: TelaJogo, jogador) -> None:
        self.desenhar(tela, jogador)

    def desenhar(self, tela: TelaJogo, jogador) -> None:
        mapa1 = pygame.image.load(self.__sprite_path)
        tela.janela.blit(mapa1, (0, 127))
        for obstaculo in self.obstaculos:
            posicao = obstaculo.hitbox.posicao
            tamanho = obstaculo.hitbox.tamanho
            color = (125, 0, 0)
            rect = pygame.Rect(posicao, tamanho)
            pygame.draw.rect(tela.janela, color, rect)

        for inimigo in self.inimigos:
            posicao = inimigo.hitbox.posicao
            tamanho = inimigo.hitbox.tamanho
            color = (0, 0, 125)
            rect = pygame.Rect(posicao, tamanho)
            pygame.draw.rect(tela.janela, color, rect)

            if inimigo.checar_atacando():
                self.desenhar_ataque(tela, inimigo)

        if jogador.checar_atacando():
            self.desenhar_ataque(tela, jogador)
        
        for item in self.itens_tela:
            item_surf= item.imagem
            item_rect = item_surf.get_rect(center = (item.posicao))
            tela.janela.blit(item_surf, item_rect)

        tamanho = jogador.hitbox.tamanho
        posicao = jogador.hitbox.posicao
        color = (0, 255, 0)
        rect = pygame.Rect(posicao, tamanho)
        pygame.draw.rect(tela.janela, color, rect)

        surface = self.jogador.status.vida()
        tela.janela.blit(surface, (0, 0))

    def validar_movimento(self, personagem: AbstractPersonagem, posicao: tuple) -> bool:
        if not isinstance(personagem, AbstractPersonagem):
            return False

        personagem_rect = pygame.Rect(posicao, personagem.hitbox.tamanho)
        terreno_rect = pygame.Rect(self.hitbox.posicao, self.hitbox.tamanho)
        jogador_rect = pygame.Rect(self.jogador.hitbox.posicao, self.jogador.hitbox.tamanho)

        # Validação com os cantos do terreno
        if personagem_rect.left < terreno_rect.left:
            return False
        if personagem_rect.right > terreno_rect.right:
            return False
        if personagem_rect.top < terreno_rect.top:
            return False
        if personagem_rect.bottom > terreno_rect.bottom:
            return False

        # Validação com todos os obstáculos do terreno
        for obstaculo in self.obstaculos:
            obstaculo_rect = pygame.Rect(obstaculo.hitbox.posicao, obstaculo.hitbox.tamanho)
            if personagem_rect.colliderect(obstaculo_rect):
                return False

        # Validação com os outros inimigos do terreno
        for inimigo in self.inimigos:
            if inimigo == personagem:  # Impede a comparação de uma mesma instância
                continue

            inimigo_rect = pygame.Rect(inimigo.hitbox.posicao, inimigo.hitbox.tamanho)
            if personagem_rect.colliderect(inimigo_rect):
                return False

        # Validação com o Jogador
        if personagem != self.jogador:
            if personagem_rect.colliderect(jogador_rect):
                return False

        return True

    def load_inimigos(self, inimigos: list) -> None:
        self.__inimigos.append(inimigos)

    def desenhar_ataque(self, tela: TelaJogo, personagem: AbstractPersonagem):
        rect_arma = personagem.get_rect_arma()
        alcance = personagem.alcance

        color = (255, 255, 255)
        pygame.draw.circle(tela.janela, color, rect_arma.center, alcance)

    def executar_ataque(self, tela: TelaJogo, personagem: AbstractPersonagem):
        self.desenhar_ataque(tela, personagem)

        rect_arma = personagem.get_rect_arma()
        for inimigo in self.inimigos:
            rect_inimigo = pygame.Rect(inimigo.hitbox.posicao, inimigo.hitbox.tamanho)

            if rect_arma.colliderect(rect_inimigo):
                dano = personagem.dano
                dano_causado = inimigo.tomar_dano(dano)

                if inimigo.vida < 1:
                    self.remover_inimigo(inimigo)

    def executar_ataque_inimigo(self, tela: TelaJogo, personagem: AbstractPersonagem):
        self.desenhar_ataque(tela, personagem)

        rect_arma = personagem.get_rect_arma()
        rect_jogador = pygame.Rect(self.jogador.hitbox.posicao, self.jogador.hitbox.tamanho)

        if rect_arma.colliderect(rect_jogador):
            dano = personagem.dano
            dano_causado = self.jogador.tomar_dano(dano)

    def mover_inimigos(self) -> None:
        for inimigo in self.inimigos:
            inimigo.mover()

    def remover_inimigo(self, inimigo):
        self.inimigos.remove(inimigo)
        self.criar_item(inimigo.hitbox.posicao)

    def load_inimigos(self, inimigos: list) -> None:
        self.inimigos.extend(inimigos)

    def is_line_of_sight_clear(self, p1, p2) -> bool:
        x1 = p1[0] // self.__opcoes.MENOR_UNIDADE
        y1 = p1[1] // self.__opcoes.MENOR_UNIDADE

        x2 = p2[0] // self.__opcoes.MENOR_UNIDADE
        y2 = p2[1] // self.__opcoes.MENOR_UNIDADE

        func = gerar_equação_vetorial_reta((x1, y1), (x2, y2))

        x = 0
        step = 0.05
        while x < 1:
            ponto = func(x)

            ponto = (int(ponto[0]), int(ponto[1]))

            cell = self.__matrix[ponto[1]][ponto[0]]
            if cell != ' ' and cell != 'J':
                return False

            x += step

        return True

    def criar_item(self, posicao):
        if len(self.__itens) !=0:
            pocao = random.choice(self.__itens)
            pocao.posicao = posicao
            self.itens_tela.append(pocao)
            self.__itens.remove(pocao)

    @property
    def jogador(self) -> Jogador:
        """Retorna a instância do Jogador que está no Terreno"""
        return self.__jogador

    @property
    def hitbox(self) -> Hitbox:
        return self.__hitbox

    @property
    def itens(self):
        return self.__itens

    @property
    def inimigos(self) -> list:
        return self.__inimigos

    @property
    def obstaculos(self) -> list:
        return self.__obstaculos
    
    @property
    def itens_tela(self):
        return self.__itens_tela

    def dropar_item(self):
        rect_jogador = pygame.Rect(self.jogador.hitbox.posicao, self.jogador.hitbox.tamanho)
        for pocao in self.itens_tela:
            item_surf= pocao.imagem
            pocao_rect = item_surf.get_rect(center = (pocao.posicao))
            if pocao_rect.colliderect(rect_jogador):
                self.itens_tela.remove(pocao)
                print("colidiu e aplicou o item")

    @abstractmethod
    def has_ended():
        pass
