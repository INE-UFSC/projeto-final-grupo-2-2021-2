from abc import ABC, abstractmethod
from typing import List
from Abstractions.AbstractObstaculo import AbstractObstaculo
from Utils.Hitbox import Hitbox
from Obstaculos.Buraco import Buraco
from Obstaculos.Parede import Parede
from Personagens.Jogador.Jogador import Jogador
from Config.Opcoes import Opcoes
from Config.TelaJogo import TelaJogo
from Abstractions.AbstractPersonagem import AbstractPersonagem
from Utils.Movement import AStar, gerar_equação_vetorial_reta
from Utils.Movement import gerar_equação_vetorial_reta
from Itens.PocaoDefesa import PocaoDefesa
from Itens.PocaoMedia import PocaoMedia
from Itens.PocaoPequena import PocaoPequena
from Itens.PocaoInvencivel import PocaoInvencivel
import pygame
import random, math


class AbstractTerreno(ABC):
    def __init__(self, inimigos: list, itens, jogador, sprite_path: str):
        self.__inimigos: List[AbstractPersonagem] = inimigos
        self.__obstaculos: List[AbstractObstaculo] = []
        self.__itens = itens
        self.__matrix = []
        self.__pontos = []

        self.__opcoes = Opcoes()
        self.__hitbox = Hitbox(posicao=(0, 0), tamanho=self.__opcoes.TAMANHO_TELA)
        self.__jogador = jogador
        self.__sprite_path = sprite_path

        #itens
        self.__itens_tela = []
        pocao_defesa = PocaoDefesa()
        pocao_media = PocaoMedia()
        pocao_invencivel = PocaoInvencivel()
        pocao_pequena = PocaoPequena()
        self.__itens.append(pocao_defesa)
        self.__itens.append(pocao_media)
        self.__itens.append(pocao_invencivel)
        self.__itens.append(pocao_pequena)
        self.__aparecer_item = 40 #porcentagem que o item tem de aparecer na tela

    def _setup_mapa(self, matriz_terreno: list) -> None:
        self.__matrix = matriz_terreno
        self.__AStar = AStar(self.__matrix, empty_points=[' ', 'J'])

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
        for obstaculo in self.__obstaculos:
            posicao = obstaculo.hitbox.posicao
            tamanho = obstaculo.hitbox.tamanho
            color = (125, 0, 0)
            rect = pygame.Rect(posicao, tamanho)
            pygame.draw.rect(tela.janela, color, rect)

        for inimigo in self.__inimigos:
            posicao = inimigo.hitbox.posicao
            tamanho = inimigo.hitbox.tamanho
            color = (0, 0, 125)
            rect = pygame.Rect(posicao, tamanho)
            pygame.draw.rect(tela.janela, color, rect)

            if inimigo.checar_atacando():
                self.__desenhar_ataque(tela, inimigo)

        # Código exclusivo para testes
        self.__desenhar_pontos(tela)

        if jogador.checar_atacando():
            self.__desenhar_ataque(tela, jogador)

        for item in self.itens_tela:
            x = item.posicao[0] 
            y = item.posicao[1]
            item_surf = item.imagem
            item_rect = item_surf.get_rect(center = (x,y))
            tela.janela.blit(item_surf, item_rect)

        tamanho = jogador.hitbox.tamanho
        posicao = jogador.hitbox.posicao
        color = (0, 255, 0)
        rect = pygame.Rect(posicao, tamanho)
        pygame.draw.rect(tela.janela, color, rect)

        surface = self.__jogador.status_tela.vida()
        tela.janela.blit(surface, (0, 0))

    # Código exclusivo para testes
    def __desenhar_pontos(self, tela: TelaJogo):
        for ponto in self.__pontos:
            rect = pygame.Rect(ponto, (2, 2))
            color = (0, 255, 255)
            pygame.draw.rect(tela.janela, color, rect)
        self.__pontos = []

    def validar_movimento(self, personagem: AbstractPersonagem, posicao: tuple) -> bool:
        if not isinstance(personagem, AbstractPersonagem):
            return False

        if personagem.hitbox.posicao == posicao:
            return True

        personagem_rect = pygame.Rect(posicao, personagem.hitbox.tamanho)
        terreno_rect = pygame.Rect(self.__hitbox.posicao, self.__hitbox.tamanho)
        jogador_rect = pygame.Rect(self.__jogador.hitbox.posicao, self.__jogador.hitbox.tamanho)

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
        for obstaculo in self.__obstaculos:
            obstaculo_rect = pygame.Rect(obstaculo.hitbox.posicao, obstaculo.hitbox.tamanho)
            if personagem_rect.colliderect(obstaculo_rect):
                return False

        # Validação com os outros inimigos do terreno
        for inimigo in self.__inimigos:
            # Inimigos não se batem
            if personagem != self.__jogador:
                break

            inimigo_rect = pygame.Rect(inimigo.hitbox.posicao, inimigo.hitbox.tamanho)
            if personagem_rect.colliderect(inimigo_rect):
                return False

        # Validação com o Jogador
        if personagem != self.__jogador:
            if personagem_rect.colliderect(jogador_rect):
                return False

        return True

    def is_line_of_sight_clear(self, p1, p2) -> bool:
        equação_vetorial = gerar_equação_vetorial_reta(p1, p2)

        x = 0.05
        step = 0.05
        while x < 1:
            ponto = equação_vetorial(x)
            # Código exclusivo para testes
            self.__pontos.append(ponto)

            if not self.__validate_normal_ponto(ponto):
                return False

            x += step
        return True

    def get_path(self, p1: tuple, p2: tuple) -> list:
        p1 = self.__reduzir_ponto(p1)
        p2 = self.__reduzir_ponto(p2)
        p1 = self.__inverter_ponto(p1)
        p2 = self.__inverter_ponto(p2)

        caminho = self.__AStar.search_path(p1, p2, True)
        for index, ponto in enumerate(caminho):
            ponto = self.__inverter_ponto(ponto)
            ponto = self.__aumentar_ponto(ponto)
            caminho[index] = ponto

        return caminho

    def get_random_path(self, p1) -> list:
        ponto_destino = self.__get_valid_reduced_point()
        while True:
            p1 = self.__reduzir_ponto(p1)
            p1 = self.__inverter_ponto(p1)

            caminho = self.__AStar.search_path(p1, ponto_destino, True)
            if len(caminho) > 0:
                for index, ponto in enumerate(caminho):
                    ponto = self.__inverter_ponto(ponto)
                    ponto = self.__aumentar_ponto(ponto)
                    caminho[index] = ponto

                return caminho

    def __get_valid_reduced_point(self) -> tuple:
        while True:
            y = random.randint(1, len(self.__matrix[0]) - 1)
            x = random.randint(6, len(self.__matrix) - 1)

            if self.__validate_reduced_ponto((x, y)):
                return (x, y)

    def mover_inimigos(self) -> None:
        for inimigo in self.__inimigos:
            inimigo.mover(self.__jogador.hitbox)

    def update(self):
        self.__jogador.update()
        for inimigo in self.__inimigos:
            inimigo.update()

    def lidar_ataques(self, tela: TelaJogo) -> None:
        if self.__jogador.verificar_ataque():
            self.__executar_ataque(tela, self.__jogador)

        for inimigo in self.__inimigos:
            if inimigo.verificar_ataque(self.__jogador.hitbox):
                if inimigo.atacar():
                    self.__executar_ataque_inimigo(tela, inimigo)

    def load_inimigos(self, inimigos: list) -> None:
        self.__inimigos.extend(inimigos)

    def __executar_ataque(self, tela: TelaJogo, personagem: AbstractPersonagem):
        self.__desenhar_ataque(tela, personagem)

        rect_arma = personagem.get_rect_arma()
        for inimigo in self.__inimigos:
            rect_inimigo = pygame.Rect(inimigo.hitbox.posicao, inimigo.hitbox.tamanho)

            if rect_arma.colliderect(rect_inimigo):
                dano = personagem.dano
                dano_causado = inimigo.tomar_dano(dano)

                if inimigo.vida < 1:
                    self.__remover_inimigo(inimigo)

    def __executar_ataque_inimigo(self, tela: TelaJogo, personagem: AbstractPersonagem):
        self.__desenhar_ataque(tela, personagem)

        rect_arma = personagem.get_rect_arma()
        rect_jogador = pygame.Rect(self.__jogador.hitbox.posicao, self.__jogador.hitbox.tamanho)

        if rect_arma.colliderect(rect_jogador):
            dano = personagem.dano
            dano_causado = self.__jogador.tomar_dano(dano)

    def __validate_reduced_ponto(self, ponto: tuple) -> bool:
        x = int(ponto[0])
        y = int(ponto[1])
        try:
            cell = self.__matrix[x][y]
        except IndexError:
            print(f'Acesso indevido a matriz em [{x}][{y}]')
            print(len(self.__matrix))
            print(len(self.__matrix[0]))
            return False

        if cell != ' ' and cell != 'J':
            return False
        else:
            return True

    def __validate_normal_ponto(self, ponto: tuple) -> bool:
        ponto = self.__reduzir_ponto(ponto)
        ponto = self.__inverter_ponto(ponto)
        return self.__validate_reduced_ponto(ponto)

    def __remover_inimigo(self, inimigo):
        self.inimigos.remove(inimigo)
        self.criar_item(inimigo.hitbox.posicao)

    def __desenhar_ataque(self, tela: TelaJogo, personagem: AbstractPersonagem):
        rect_arma = personagem.get_rect_arma()
        alcance = personagem.alcance

        color = (255, 255, 255)
        pygame.draw.circle(tela.janela, color, rect_arma.center, alcance)

    def __reduzir_ponto(self, ponto: tuple) -> tuple:
        x = ponto[0] // self.__opcoes.MENOR_UNIDADE
        y = ponto[1] // self.__opcoes.MENOR_UNIDADE

        return (int(x), int(y))

    def __aumentar_ponto(self, ponto: tuple) -> tuple:
        x = ponto[0] * self.__opcoes.MENOR_UNIDADE
        y = ponto[1] * self.__opcoes.MENOR_UNIDADE

        return (x, y)

    def __centralizar_ponto(self, ponto: tuple) -> tuple:
        x = ponto[0] + self.__opcoes.MENOR_UNIDADE
        y = ponto[1] + self.__opcoes.MENOR_UNIDADE

        return (x, y)

    def __inverter_ponto(self, ponto: tuple) -> tuple:
        return (ponto[1], ponto[0])

    def criar_item(self, posicao):
        chance_aparecer = math.ceil(100*random.random()) #sorteia um numero entre 1 e 100
        if chance_aparecer > self.aparecer_item:
            if len(self.__itens) != 0:
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
    
    @property
    def aparecer_item(self):
        return self.__aparecer_item

    def dropar_item(self):
        rect_jogador = pygame.Rect(self.jogador.hitbox.posicao, self.jogador.hitbox.tamanho)
        for pocao in self.itens_tela:
            item_surf = pocao.imagem
            pocao_rect = item_surf.get_rect(center=(pocao.posicao))
            if pocao_rect.colliderect(rect_jogador):
                self.__jogador.receber_item(pocao)
                self.itens_tela.remove(pocao)
                

    @abstractmethod
    def has_ended():
        pass
