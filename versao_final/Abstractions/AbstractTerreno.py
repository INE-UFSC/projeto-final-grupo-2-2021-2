from abc import ABC, abstractmethod
from configparser import InterpolationMissingOptionError
from math import ceil
from typing import List

import pygame
from Abstractions.AbstractInimigo import AbstractInimigo
from Abstractions.AbstractItem import AbstractItem
from Abstractions.AbstractObjeto import AbstractObjeto
from Utils.Hitbox import Hitbox
from Personagens.Jogador.Jogador import Jogador
from Config.Opcoes import Opcoes
from Config.TelaJogo import TelaJogo
from Abstractions.AbstractPersonagem import AbstractPersonagem
from Utils.Maps import MapUpdater
from Utils.Movement import AStar, distancia_dois_pontos, gerar_equação_vetorial_reta
from Utils.Movement import gerar_equação_vetorial_reta
from Itens.PocaoDefesa import PocaoDefesa
from Itens.PocaoMedia import PocaoMedia
from Itens.PocaoPequena import PocaoPequena
from Itens.PocaoInvencivel import PocaoInvencivel
from pygame import Surface, Rect, draw, font
from random import random, choice, randint


class AbstractTerreno(ABC):
    def __init__(self, inimigos: list, itens: list, jogador: Jogador):
        self.__inimigos: List[AbstractInimigo] = inimigos
        self.__itens: List[AbstractItem] = itens
        self.__objetos: List[AbstractObjeto] = []
        self.__matrix = []
        self.__pontos = []

        self.__opcoes = Opcoes()
        self.__hitbox = Hitbox(self.__opcoes.POSICAO_MAPAS, self.__opcoes.TAMANHO_MAPAS)
        self.__jogador = jogador

        # itens
        self.__itens_tela = []
        pocao_defesa = PocaoDefesa()
        pocao_media = PocaoMedia()
        pocao_invencivel = PocaoInvencivel()
        pocao_pequena = PocaoPequena()
        self.__itens.append(pocao_defesa)
        self.__itens.append(pocao_media)
        self.__itens.append(pocao_invencivel)
        self.__itens.append(pocao_pequena)
        self.__aparecer_item = 40  # porcentagem que o item tem de aparecer na tela

    def _setup_mapa(self, matriz_terreno: list) -> None:
        self.__matrix = matriz_terreno
        self.__configure_pathfinders()

    def iniciar_rodada(self, tela: TelaJogo, jogador) -> None:
        self.desenhar(tela, jogador)

    def desenhar(self, tela: TelaJogo, jogador) -> None:
        tela.janela.blit(self.image, self.rect)

        for objeto in self.__objetos:
            objeto.desenhar(tela)

        for inimigo in self.__inimigos:
            posicao = inimigo.hitbox.posicao
            tamanho = inimigo.hitbox.tamanho
            color = (0, 0, 125)
            rect = Rect(posicao, tamanho)
            # Desenha os hitbox deles
            draw.rect(tela.janela, color, rect)

            inimigo.animate()
            tela.janela.blit(inimigo.image, inimigo.rect)

        # Código para desenhar ataque realizado, será removido posteriormente
        if jogador.checar_atacando():
            self.__desenhar_ataque(tela, jogador)

        for item in self.__itens_tela:
            x = item.posicao[0]
            y = item.posicao[1]
            item_surf = item.imagem
            item_rect = item_surf.get_rect(center=(x, y))
            tela.janela.blit(item_surf, item_rect)

        # self.__desenhar_pontos(tela)

        tamanho = jogador.hitbox.tamanho
        posicao = jogador.hitbox.posicao
        color = (0, 255, 0)
        rect = Rect(posicao, tamanho)
        draw.rect(tela.janela, color, rect)

        surface = self.__jogador.status_tela.vida()
        tela.janela.blit(surface, (0, 0))

    def criar_item(self, posicao):
        chance_aparecer = ceil(100*random())  # sorteia um numero entre 1 e 100
        if chance_aparecer > self.__aparecer_item:
            if len(self.__itens) != 0:
                pocao = choice(self.__itens)
                pocao.posicao = posicao
                self.__itens_tela.append(pocao)
                self.__itens.remove(pocao)

    def dropar_item(self):
        rect_jogador = Rect(self.__jogador.hitbox.posicao, self.__jogador.hitbox.tamanho)
        for pocao in self.__itens_tela:
            item_surf = pocao.imagem
            pocao_rect = item_surf.get_rect(center=(pocao.posicao))
            if pocao_rect.colliderect(rect_jogador):
                self.__jogador.receber_item(pocao)
                self.__itens_tela.remove(pocao)

    def validar_movimento(self, personagem: AbstractPersonagem, posicao: tuple) -> bool:
        if not isinstance(personagem, AbstractPersonagem):
            return False

        if personagem.hitbox.posicao == posicao:
            return True

        if not self._posicao_index_valido(posicao):
            return False

        if self._posicao_bloqueia_movimento(posicao):
            return False

        if not self._hitbox_cabe_na_posicao(personagem.hitbox, posicao):
            return False

        personagem_rect = Rect(posicao, personagem.hitbox.tamanho)
        jogador_rect = Rect(self.__jogador.hitbox.posicao, self.__jogador.hitbox.tamanho)

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
        distancia = distancia_dois_pontos(p1, p2)

        distancia_entre_pixels_checados = 4
        step = 1 / (distancia // distancia_entre_pixels_checados)

        x = 0
        while x < 1:
            ponto = equação_vetorial(x)
            # Código exclusivo para testes
            self.__pontos.append(ponto)

            if self._posicao_bloqueia_visao(ponto):
                return False

            x += step
        return True

    def get_path(self, hitbox: Hitbox, p2: tuple) -> list:
        p1 = self._remove_offset_from_point(hitbox.posicao)
        p2 = self._remove_offset_from_point(p2)
        p1 = self._reduzir_ponto(p1)
        p2 = self._reduzir_ponto(p2)
        p1 = self._inverter_ponto(p1)
        p2 = self._inverter_ponto(p2)

        pathfinder = self.__get_AStar_pathfinder_for_hitbox(hitbox)
        caminho = pathfinder.search_path(p1, p2, True)
        for index, ponto in enumerate(caminho):
            ponto = self._inverter_ponto(ponto)
            ponto = self._aumentar_ponto(ponto)
            ponto = self._apply_offset_to_point(ponto)
            caminho[index] = ponto

        return caminho

    def get_random_path(self, hitbox: Hitbox) -> list:
        ponto_destino = self.__get_valid_destiny_point_for_hitbox(hitbox)
        while True:
            p1 = self._remove_offset_from_point(hitbox.posicao)
            p1 = self._reduzir_ponto(p1)
            p1 = self._inverter_ponto(p1)

            pathfinder = self.__get_AStar_pathfinder_for_hitbox(hitbox)
            caminho = pathfinder.search_path(p1, ponto_destino, True)
            if len(caminho) > 0:
                for index, ponto in enumerate(caminho):
                    ponto = self._inverter_ponto(ponto)
                    ponto = self._aumentar_ponto(ponto)
                    ponto = self._apply_offset_to_point(ponto)
                    caminho[index] = ponto

            return caminho

    def mover_inimigos(self) -> None:
        for inimigo in self.__inimigos:
            inimigo.mover(self.__jogador.hitbox)

    def update(self):
        self.__jogador.update()
        for inimigo in self.__inimigos:
            inimigo.update(self.__jogador.hitbox)

            if inimigo.morreu:
                self.__remover_inimigo(inimigo)

    def lidar_ataques(self, tela: TelaJogo) -> None:
        if self.__jogador.verificar_ataque():
            self.__executar_ataque(tela, self.__jogador)

        for inimigo in self.__inimigos:
            if inimigo.atacar():
                self.__executar_ataque_inimigo(tela, inimigo)

    def load_inimigos(self, inimigos: list) -> None:
        self.__inimigos.extend(inimigos)

    def __executar_ataque(self, tela: TelaJogo, personagem: AbstractPersonagem):
        self.__desenhar_ataque(tela, personagem)

        rect_arma = personagem.get_rect_arma()
        for inimigo in self.__inimigos:
            rect_inimigo = Rect(inimigo.hitbox.posicao, inimigo.hitbox.tamanho)

            if rect_arma.colliderect(rect_inimigo):
                dano = personagem.dano
                dano_causado = inimigo.tomar_dano(dano)

    def __executar_ataque_inimigo(self, tela: TelaJogo, personagem: AbstractPersonagem):
        self.__desenhar_ataque(tela, personagem)

        rect_arma = personagem.get_rect_arma()
        rect_jogador = Rect(self.__jogador.hitbox.posicao, self.__jogador.hitbox.tamanho)

        if rect_arma.colliderect(rect_jogador):
            dano = personagem.dano
            dano_causado = self.__jogador.tomar_dano(dano)

    def __get_AStar_pathfinder_for_hitbox(self, hitbox: Hitbox) -> AStar:
        proporcao = self._get_proporsion_for_hitbox(hitbox)

        if proporcao in self.__proporcao_to_pathfinders.keys():
            return self.__proporcao_to_pathfinders[proporcao]
        else:
            matrix = self._get_reduced_matrix_for_proporsion(proporcao)
            pathfinder = AStar(matrix, [' ', 'J'], ['X'])

            self.__proporcao_to_matrix[proporcao] = matrix
            self.__proporcao_to_pathfinders[proporcao] = pathfinder
            return pathfinder

    def __configure_pathfinders(self):
        self.__proporcao_to_matrix = {}
        self.__proporcao_to_pathfinders = {}
        self.__MapUpdater = MapUpdater(self.__matrix, 'X', ['J', ' '], ['P, 0'])

        matrix_1_1 = self._get_reduced_matrix_for_proporsion((1, 1))
        matrix_1_2 = self._get_reduced_matrix_for_proporsion((1, 2))
        matrix_2_1 = self._get_reduced_matrix_for_proporsion((2, 1))
        matrix_2_2 = self._get_reduced_matrix_for_proporsion((2, 2))

        pathfinder_1_1 = AStar(matrix_1_1, [' ', 'J'], ['X'])
        pathfinder_1_2 = AStar(matrix_1_2, [' ', 'J'], ['X'])
        pathfinder_2_1 = AStar(matrix_2_1, [' ', 'J'], ['X'])
        pathfinder_2_2 = AStar(matrix_2_2, [' ', 'J'], ['X'])

        self.__proporcao_to_pathfinders = {
            (1, 1): pathfinder_1_1,
            (1, 2): pathfinder_1_2,
            (2, 1): pathfinder_2_1,
            (2, 2): pathfinder_2_2,
        }
        self.__proporcao_to_matrix = {
            (1, 1): matrix_1_1,
            (1, 2): matrix_1_2,
            (2, 1): matrix_2_1,
            (2, 2): matrix_2_2,
        }

    def _get_reduced_matrix_for_proporsion(self, proporsion: tuple) -> list:
        if proporsion in self.__proporcao_to_matrix.keys():
            return self.__proporcao_to_matrix[proporsion]

        try:
            updated_map = self.__MapUpdater.update_map_for_size(proporsion)
            return updated_map
        except Exception as e:
            print(f'Erro na criação do mapa: {e}')
            return self.__matrix

    def __get_valid_destiny_point_for_hitbox(self, hitbox: Hitbox) -> tuple:
        proporcao = self._get_proporsion_for_hitbox(hitbox)
        matrix = self._get_reduced_matrix_for_proporsion(proporcao)

        while True:
            y = randint(1, len(self.__matrix[0]) - 1)
            x = randint(1, len(self.__matrix) - 1)

            if self._validate_inverted_ponto_in_matrix((x, y), matrix):
                return (x, y)

    def _get_proporsion_for_hitbox(self, hitbox: Hitbox) -> tuple:
        proporsion_y = hitbox.tamanho[0] / self.__opcoes.MENOR_UNIDADE
        proporsion_x = hitbox.tamanho[1] / self.__opcoes.MENOR_UNIDADE

        return (ceil(proporsion_x), ceil(proporsion_y))

    def _validate_inverted_ponto_in_matrix(self, ponto: tuple, matrix: list) -> bool:
        x = int(ponto[0])
        y = int(ponto[1])

        if x < 0 or x >= len(matrix):
            print(f'Acesso indevido a matriz em [{x}][{y}] - 1')
            return False

        if y < 0 or y >= len(matrix[0]):
            print(f'Acesso indevido a matriz em [{x}][{y}] - 2')
            return False

        if matrix[x][y] != ' ' and matrix[x][y] != 'J':
            return False

        return True

    def __validate_reduced_ponto_for_obstaculo(self, ponto: tuple) -> bool:
        x = int(ponto[0])
        y = int(ponto[1])

        if x < 0 or x >= len(self.__matrix):
            print(f'Acesso indevido a matriz em [{x}][{y}] - 3')
            return False

        if y < 0 or y >= len(self.__matrix[0]):
            print(f'Acesso indevido a matriz em [{x}][{y}] - 4')
            return False

        if self.__matrix[x][y] == 'P':
            return False

        return True

    def __validate_normal_ponto_for_obstaculo(self, ponto: tuple) -> bool:
        ponto = self._remove_offset_from_point(ponto)
        ponto = self._reduzir_ponto(ponto)
        ponto = self._inverter_ponto(ponto)
        return self.__validate_reduced_ponto_for_obstaculo(ponto)

    def _remove_offset_from_point(self, ponto: tuple) -> tuple:
        return (ponto[0], ponto[1] - self.__opcoes.POSICAO_MAPAS[1])

    def _apply_offset_to_point(self, position: tuple) -> tuple:
        return (position[0], position[1] + self.__opcoes.POSICAO_MAPAS[1])

    def _hitbox_cabe_na_posicao(self, hitbox: Hitbox, posicao: tuple) -> bool:
        proporsion = self._get_proporsion_for_hitbox(hitbox)
        matrix = self._get_reduced_matrix_for_proporsion(proporsion)
        ponto = self._remove_offset_from_point(posicao)
        ponto = self._reduzir_ponto(ponto)
        ponto = self._inverter_ponto(ponto)
        return self._validate_inverted_ponto_in_matrix(ponto, matrix)

    # Código exclusivo para testes
    def __desenhar_pontos(self, tela: TelaJogo):
        for ponto in self.__pontos:
            rect = Rect(ponto, (2, 2))
            color = (0, 255, 255)
            draw.rect(tela.janela, color, rect)
        self.__pontos = []

    # Código exclusivo para testes
    def __desenhar_quadrados(self, tela: TelaJogo):
        return
        for index, linha in enumerate(self.__matrix):
            for index_column, coluna in enumerate(linha):
                posicao = self.__aumentar_ponto((index_column, index))
                posicao = self.__apply_offset_to_point(posicao)

                if index % 2 == 0:
                    if index_column % 2 == 0:
                        color = (255, 125, 125)
                    else:
                        color = (125, 125, 255)
                else:
                    if index_column % 2 == 0:
                        color = (125, 125, 255)
                    else:
                        color = (255, 125, 125)

                text = f'{index_column} - {index}'
                fonte = font.SysFont('arial', 8, True, False)
                texto_formatado = fonte.render(text, True, (0, 0, 0))

                rect = Rect(posicao, (self.__opcoes.MENOR_UNIDADE, self.__opcoes.MENOR_UNIDADE))
                draw.rect(tela.janela, color, rect)
                tela.janela.blit(texto_formatado, posicao)

    def __remover_inimigo(self, inimigo):
        self.__inimigos.remove(inimigo)
        self.criar_item(inimigo.hitbox.posicao)

    def __desenhar_ataque(self, tela: TelaJogo, personagem: AbstractPersonagem):
        rect_arma = personagem.get_rect_arma()
        alcance = personagem.alcance

        color = (255, 255, 255)
        draw.circle(tela.janela, color, rect_arma.center, alcance)

    def _reduzir_ponto(self, ponto: tuple) -> tuple:
        x = ponto[0] // self.__opcoes.MENOR_UNIDADE
        y = ponto[1] // self.__opcoes.MENOR_UNIDADE

        return (int(x), int(y))

    def _aumentar_ponto(self, ponto: tuple) -> tuple:
        x = ponto[0] * self.__opcoes.MENOR_UNIDADE
        y = ponto[1] * self.__opcoes.MENOR_UNIDADE

        return (x, y)

    def _inverter_ponto(self, ponto: tuple) -> tuple:
        return (ponto[1], ponto[0])

    @property
    def jogador(self) -> Jogador:
        """Retorna a instância do Jogador que está no Terreno"""
        return self.__jogador

    @property
    def inimigos(self) -> List[AbstractInimigo]:
        return self.__inimigos

    @property
    def objetos(self) -> List[AbstractObjeto]:
        return self.__objetos

    @abstractmethod
    def has_ended():
        pass

    @property
    def _opcoes(self) -> Opcoes:
        return self.__opcoes

    @property
    def hitbox(self) -> Hitbox:
        return self.__hitbox

    @property
    @abstractmethod
    def image(self) -> Surface:
        pass

    @property
    @abstractmethod
    def rect(self) -> Rect:
        pass

    @abstractmethod
    def _posicao_bloqueia_visao() -> bool:
        pass

    @abstractmethod
    def _posicao_bloqueia_movimento() -> bool:
        pass

    @abstractmethod
    def _posicao_index_valido() -> bool:
        pass
