from abc import ABC, abstractmethod
from math import ceil
from typing import List, Type
from Personagens.AbstractInimigo import AbstractInimigo
from Itens.AbstractItem import AbstractItem
from Mapas.MapInterpreter import MapInterpreter
from Objetos.AbstractObjeto import AbstractObjeto
from Objetos.ObstaculoInvisivel import ObjetoInvisivel
from Personagens.AbstractSignal import AbstractSignal
from Utils.Adapter import Adapter
from Utils.Hitbox import Hitbox
from Personagens.Jogador import Jogador
from Config.Opcoes import Opcoes
from Config.TelaJogo import TelaJogo
from Personagens.AbstractPersonagem import AbstractPersonagem
from Utils.Maps import MapUpdater
from Utils.Movement import AStar, GAHandler
from pygame import Surface, Rect, draw
from random import randint


class AbstractMapa(ABC):
    def __init__(self, jogador: Jogador, enemies: List[Type[AbstractInimigo]]):
        self.__adapter = Adapter()
        self.__opcoes = Opcoes()
        self.__enemies_types: List[Type[AbstractInimigo]] = enemies

        self.__inimigos: List[AbstractInimigo] = []
        self.__objetos: List[AbstractObjeto] = []
        self.__itens: List[AbstractItem] = []
        self.__itens_to_duration = {}
        self.__matrix = []
        self.__pontos = []
        self.__jogador = jogador

        self.__hitbox = Hitbox(self.__opcoes.POSICAO_MAPAS, self.__opcoes.TAMANHO_MAPAS)

    @abstractmethod
    def load(self):
        self.__inimigos.extend(self.__create_enemies(self.__enemies_types))

    def _setup_mapa(self, mapa_matrix: list) -> None:
        self.__proporcao_to_matrix = {}
        self.__proporcao_to_pathfinders = {}

        self.__map = MapInterpreter(mapa_matrix)
        self.__matrix = self.__map.get_matrix_only_obstacles()
        self.__configure_pathfinders()

        player_pos = self.__map.player_start_position
        player_pos = self.__adapter.matrix_index_to_pygame_pos(player_pos)
        self.__jogador.hitbox.posicao = player_pos

        menor = self._opcoes.MENOR_UNIDADE

        for position_map in self.__map.positions_blocking_movement_and_vision:
            position = self.__adapter.matrix_index_to_pygame_pos(position_map)
            self.__objetos.append(ObjetoInvisivel(position, (menor, menor), False, True))

        for position_map in self.__map.positions_blocking_only_vision:
            position = self.__adapter.matrix_index_to_pygame_pos(position_map)
            self.__objetos.append(ObjetoInvisivel(position, (menor, menor), True, True))

        for position_map in self.__map.positions_blocking_only_movement:
            position = self.__adapter.matrix_index_to_pygame_pos(position_map)
            self.__objetos.append(ObjetoInvisivel(position, (menor, menor), False, False))

        for position_map in self.__map.positions_blocking_nothing:
            position = self.__adapter.matrix_index_to_pygame_pos(position_map)
            self.__objetos.append(ObjetoInvisivel(position, (menor, menor), True, False))

    def iniciar_rodada(self, tela: TelaJogo) -> None:
        self.desenhar(tela)

    def send_enemies_signal(self, signal: AbstractSignal) -> None:
        for enemy in self.__inimigos:
            if enemy == signal.sender:
                continue

            dist = GAHandler.distancia_dois_pontos(signal.source_position, enemy.hitbox.center)
            if dist < signal.signal_range:
                enemy.receive_signal(signal)

    def animate(self) -> None:
        for inimigo in self.__inimigos:
            inimigo.animate()
        self.__jogador.animate()

    def desenhar(self, tela: TelaJogo) -> None:
        tela.janela.blit(self.image, self.rect)

        for objeto in self.__objetos:
            objeto.desenhar(tela)

        for item in self.__itens:
            duration = self.__itens_to_duration[item]
            if duration > 100:
                tela.janela.blit(item.image, item.rect)
            else:
                if duration % 4 == 0:
                    tela.janela.blit(item.image, item.rect)

        for inimigo in self.__inimigos:
            tela.janela.blit(inimigo.image, inimigo.rect)

        self.__desenhar_pontos(tela)
        tela.janela.blit(self.__jogador.image, self.__jogador.rect)

        rect_escudo = self.__jogador.get_rect_escudo()
        color = (0, 0, 255)
        draw.rect(tela.janela, color, rect_escudo)

    def pegar_item(self) -> AbstractItem:
        rect_jogador = Rect(self.__jogador.hitbox.posicao, self.__jogador.hitbox.tamanho)
        for item in self.__itens:
            if rect_jogador.colliderect(item.rect):
                self.__jogador.receber_item(item)
                self.__itens.remove(item)
                self.__itens_to_duration.pop(item)

    def validar_movimento(self, personagem: AbstractPersonagem, posicao: tuple) -> bool:
        if not isinstance(personagem, AbstractPersonagem):
            return False

        if personagem.hitbox.posicao == posicao:
            return True

        posicao_matrix = self.__adapter.pygame_pos_to_matrix_index(posicao)
        if not self.__map.is_position_valid(posicao_matrix):
            return False

        if posicao_matrix in self.__map.positions_blocking_movement:
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
            if inimigo.hitbox.transpassavel:
                break

            inimigo_rect = Rect(inimigo.hitbox.posicao, inimigo.hitbox.tamanho)
            if personagem_rect.colliderect(inimigo_rect):
                return False

        for objeto in self.__objetos:
            if not objeto.transpassavel:
                objeto_rect = Rect(objeto.hitbox.posicao, objeto.hitbox.tamanho)
                if objeto_rect.colliderect(personagem_rect):
                    return False

        # Validação com o Jogador
        if personagem != self.__jogador:
            if personagem_rect.colliderect(jogador_rect):
                return False

        return True

    def is_line_of_sight_clear(self, p1, p2) -> bool:
        equação_vetorial = GAHandler.gerar_equação_vetorial_reta(p1, p2)
        distancia = GAHandler.distancia_dois_pontos(p1, p2)

        distancia_entre_pixels_checados = 4
        step = 1 / (distancia // distancia_entre_pixels_checados)

        x = 0
        while x < 1:
            ponto = equação_vetorial(x)
            # Código exclusivo para testes
            # self.__pontos.append(ponto)

            ponto = self.__adapter.pygame_pos_to_matrix_index(ponto)

            if ponto in self.__map.positions_blocking_vision:
                return False

            x += step
        return True

    def is_line_of_sight_clear_to_walk(self, p1, p2) -> bool:
        equação_vetorial = GAHandler.gerar_equação_vetorial_reta(p1, p2)
        distancia = GAHandler.distancia_dois_pontos(p1, p2)

        distancia_entre_pixels_checados = 4
        step = 1 / (distancia // distancia_entre_pixels_checados)

        x = 0
        while x < 1:
            ponto = equação_vetorial(x)
            # Código exclusivo para testes
            # self.__pontos.append(ponto)

            ponto = self.__adapter.pygame_pos_to_matrix_index(ponto)
            if ponto in self.__map.positions_blocking_movement:
                return False

            x += step
        return True

    def get_path(self, hitbox: Hitbox, p2: tuple) -> list:
        p1 = self.__adapter.pygame_pos_to_matrix_index(hitbox.posicao)
        p2 = self.__adapter.pygame_pos_to_matrix_index(p2)

        pathfinder = self.__get_AStar_pathfinder_for_hitbox(hitbox)
        caminho = pathfinder.search_path(p1, p2, True)
        for index, ponto in enumerate(caminho):
            caminho[index] = self.__adapter.matrix_index_to_pygame_pos(ponto)

        return caminho

    def get_random_path(self, hitbox: Hitbox) -> list:
        ponto_destino = self.__get_valid_destiny_point_for_hitbox(hitbox)
        while True:
            p1 = self.__adapter.pygame_pos_to_matrix_index(hitbox.posicao)

            pathfinder = self.__get_AStar_pathfinder_for_hitbox(hitbox)
            caminho = pathfinder.search_path(p1, ponto_destino, True)
            if len(caminho) > 0:
                for index, ponto in enumerate(caminho):
                    caminho[index] = self.__adapter.matrix_index_to_pygame_pos(ponto)

            return caminho

    def mover_inimigos(self) -> None:
        for inimigo in self.__inimigos:
            inimigo.mover(self.__jogador.hitbox)

    def update(self):
        self.__jogador.update()
        for inimigo in self.__inimigos:
            inimigo.update(self.__jogador.hitbox)

            if inimigo.morreu:
                self.__handle_item_drop(inimigo.hitbox.center)
                self.__remover_inimigo(inimigo)

        for item in self.__itens:
            duration = self.__itens_to_duration[item]
            self.__itens_to_duration[item] = duration - 1
            if duration < 0:
                self.__itens_to_duration.pop(item)
                self.__itens.remove(item)

    def __handle_item_drop(self, position: tuple) -> None:
        item = self._get_item_to_drop()
        if isinstance(item, AbstractItem):
            item.posicao = position
            self.__itens.append(item)
            self.__itens_to_duration[item] = self.__opcoes.ITENS_DROPPED_DURATION

    def change_player_position_entering_map(self):
        start_player_position = self.__map.player_start_position
        start_player_position = self.__adapter.matrix_index_to_pygame_pos(start_player_position)

        self.__jogador.hitbox.posicao = start_player_position

    def change_player_position_returning_map(self):
        return_player_position = self.__map.player_return_position
        return_player_position = self.__adapter.matrix_index_to_pygame_pos(return_player_position)

        self.__jogador.hitbox.posicao = return_player_position

    def lidar_ataques(self) -> None:
        if self.__jogador.atacar():
            self.__executar_ataque(self.__jogador)

        for inimigo in self.__inimigos:
            if inimigo.atacar():
                self.__executar_ataque_inimigo(inimigo)

    def load_inimigos(self, inimigos: list) -> None:
        self.__inimigos.extend(inimigos)

    def __executar_ataque(self, personagem: AbstractPersonagem):
        ponto1 = personagem.hitbox.center
        pontos_2 = personagem.pontos_para_ataque()

        pontos = []
        for ponto2 in pontos_2:
            func = GAHandler.gerar_equação_vetorial_reta(ponto1, ponto2)

            x = 0.6
            step = 0.2
            alcance = self.__adapter.alcance_to_vector_dist(personagem.alcance)
            while x < alcance:
                ponto = func(x)

                # Código para testes
                self.__pontos.append(ponto)
                pontos.append(ponto)
                x += step

        for inimigo in self.__inimigos:
            rect_inimigo = Rect(inimigo.hitbox.posicao, inimigo.hitbox.tamanho)

            for ponto in pontos:
                if rect_inimigo.collidepoint(ponto):
                    dano = personagem.dano
                    dano_causado = inimigo.tomar_dano(dano)
                    break

    def __executar_ataque_inimigo(self, personagem: AbstractPersonagem):
        ponto1 = personagem.hitbox.center
        pontos_2 = personagem.pontos_para_ataque()

        pontos = []
        for ponto2 in pontos_2:
            func = GAHandler.gerar_equação_vetorial_reta(ponto1, ponto2)

            x = 0.6
            step = 0.2
            alcance = self.__adapter.alcance_to_vector_dist(personagem.alcance)
            while x < alcance:
                ponto = func(x)

                # Código para testes
                self.__pontos.append(ponto)
                pontos.append(ponto)
                x += step

        acertou_jogador = False
        rect_jogador = Rect(self.__jogador.hitbox.posicao, self.__jogador.hitbox.tamanho)
        for ponto in pontos:
            if rect_jogador.collidepoint(ponto):
                acertou_jogador = True
                break

        acertou_escudo = False
        for ponto in pontos:
            rect_escudo = self.__jogador.get_rect_escudo()
            if rect_escudo.collidepoint(ponto):
                acertou_escudo = True
                break

        if acertou_escudo:
            dano = personagem.dano
            self.__jogador.tomar_dano_escudo(dano)
        elif acertou_jogador:
            dano = personagem.dano
            dano_causado = self.__jogador.tomar_dano(dano)

    def __get_AStar_pathfinder_for_hitbox(self, hitbox: Hitbox) -> AStar:
        proporcao = self._get_proporsion_for_hitbox(hitbox)

        if proporcao in self.__proporcao_to_pathfinders.keys():
            return self.__proporcao_to_pathfinders[proporcao]
        else:
            matrix = self._get_reduced_matrix_for_proporsion(proporcao)
            pathfinder = AStar(matrix, [' '], ['X'])

            self.__proporcao_to_matrix[proporcao] = matrix
            self.__proporcao_to_pathfinders[proporcao] = pathfinder
            return pathfinder

    def __configure_pathfinders(self):
        self.__proporcao_to_matrix = {}
        self.__proporcao_to_pathfinders = {}
        self.__MapUpdater = MapUpdater(self.__matrix)

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
            self.__proporcao_to_matrix[proporsion] = updated_map
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

            if self.__MapUpdater.validate_ponto_in_matrix((x, y), matrix):
                return (x, y)

    def _get_proporsion_for_hitbox(self, hitbox: Hitbox) -> tuple:
        proporsion_y = hitbox.tamanho[0] / self.__opcoes.MENOR_UNIDADE
        proporsion_x = hitbox.tamanho[1] / self.__opcoes.MENOR_UNIDADE

        return (ceil(proporsion_x), ceil(proporsion_y))

    def _hitbox_cabe_na_posicao(self, hitbox: Hitbox, posicao: tuple) -> bool:
        proporsion = self._get_proporsion_for_hitbox(hitbox)
        matrix = self._get_reduced_matrix_for_proporsion(proporsion)
        ponto = self.__adapter.pygame_pos_to_matrix_index(posicao)

        return self.__MapUpdater.validate_ponto_in_matrix(ponto, matrix)

    def __create_enemies(self, enemies_types: List[Type[AbstractInimigo]]) -> List[AbstractInimigo]:
        enemies_list: List[AbstractInimigo] = []
        posicoes = self.__map.get_enemies_positions()
        index = 0

        for Enemy_Type in enemies_types:
            position = posicoes[index]
            index += 1
            if index >= len(posicoes):
                index = 0

            position = self.__adapter.matrix_index_to_pygame_pos(position)

            enemy = Enemy_Type(mapa=self, posicao=position)
            enemies_list.append(enemy)

        return enemies_list

    # Código exclusivo para testes
    def __desenhar_pontos(self, tela: TelaJogo):
        for ponto in self.__pontos:
            rect = Rect(ponto, (2, 2))
            color = (0, 255, 255)
            draw.rect(tela.janela, color, rect)
        self.__pontos = []

    def __remover_inimigo(self, inimigo):
        self.__inimigos.remove(inimigo)

    @property
    def jogador(self) -> Jogador:
        return self.__jogador

    @property
    def inimigos(self) -> List[AbstractInimigo]:
        return self.__inimigos

    @property
    def objetos(self) -> List[AbstractObjeto]:
        return self.__objetos

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
    def _get_item_to_drop() -> AbstractItem:
        pass

    @abstractmethod
    def go_next_map() -> bool:
        pass

    @abstractmethod
    def go_previous_map() -> bool:
        pass

    @property
    @abstractmethod
    def loaded(self) -> bool:
        pass

    @property
    def _map(self) -> MapInterpreter:
        return self.__map
