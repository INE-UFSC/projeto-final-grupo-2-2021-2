from abc import ABC, abstractmethod
from Utils.Hitbox import Hitbox
from Abstractions.AbstractPersonagem import AbstractPersonagem
from Enums.Enums import Direction
from Abstractions.AbstractTerreno import AbstractTerreno
import pygame


class AbstractInimigo(AbstractPersonagem, ABC):
    def __init__(self, stats: dict, posicao: tuple, tamanho: tuple, terreno: AbstractTerreno, sprite_paths) -> None:
        self.__direction = Direction.MEIO_BAIXO
        self.__em_repouso = True
        self.__destino = None
        self.__view_distance = stats['view_distance'] if 'view_distance' in stats.keys() else 15

        super().__init__(stats, posicao, tamanho, terreno, sprite_paths)

    def update_visao(self, hit_jogador: Hitbox) -> None:
        if self.__em_repouso:
            if self.__esta_vendo_jogador(hit_jogador):
                self.__em_repouso = False

    def mover(self, hit_jogador: Hitbox) -> None:
        if self.__em_repouso:
            return None

        if self.__destino is None:
            self.__destino = self.terreno.get_destino(self.hitbox.posicao, hit_jogador.posicao)

        if self.__destino is None:
            rect_jogador = pygame.Rect(hit_jogador.posicao, hit_jogador.tamanho)
            center_jogador = rect_jogador.center

            self.__dumb_movement(hit_jogador)
        else:
            self.__mover_destino()

    def __dumb_movement(self, hit_jogador: Hitbox) -> None:
        rect_jogador = pygame.Rect(hit_jogador.posicao, hit_jogador.tamanho)
        center_jogador = rect_jogador.center

        if center_jogador[0] > self.hitbox.x:
            x_movement = self.vel
        elif center_jogador[0] < self.hitbox.x:
            x_movement = - self.vel
        else:
            x_movement = 0

        if center_jogador[1] > self.hitbox.y:
            y_movement = self.vel
        elif center_jogador[1] < self.hitbox.y:
            y_movement = - self.vel
        else:
            y_movement = 0

        nova_posicao_x = (self.hitbox.x + x_movement, self.hitbox.y)
        if self.terreno.validar_movimento(personagem=self, posicao=nova_posicao_x):
            self.hitbox.posicao = nova_posicao_x

        nova_posicao_y = (self.hitbox.x, self.hitbox.y + y_movement)
        if self.terreno.validar_movimento(personagem=self, posicao=nova_posicao_y):
            self.hitbox.posicao = nova_posicao_y

        self._atualizar_sprite(x_movement, y_movement)
        self.__atualizar_frente(x_movement, y_movement)

    def verificar_ataque(self, hit_jogador: Hitbox):
        distancia = self.__calcular_distancia(hit_jogador)

        if distancia < self.arma.alcance:
            return True
        else:
            return False

    def get_rect_arma(self) -> pygame.Rect:
        posicao_frente = self.__determinar_posicao_frente()

        rect = pygame.Rect(posicao_frente, (self.alcance, self.alcance))
        rect.center = posicao_frente
        return rect

    def atacar(self):
        if self.arma.atacar():
            return True
        else:
            return False

    def __esta_vendo_jogador(self, hit_jogador: Hitbox) -> bool:
        distancia = self.__calcular_distancia(hit_jogador)
        if distancia > self.__view_distance:
            return False

        esta_vendo = self.terreno.is_line_of_sight_clear(self.hitbox.posicao, hit_jogador.posicao)
        if esta_vendo:
            return True
        else:
            return False

    def __mover_destino(self):
        if self.__destino[0] > self.hitbox.x:
            x_movement = self.vel
        elif self.__destino[0] < self.hitbox.x:
            x_movement = -self.vel
        else:
            x_movement = 0

        if self.__destino[1] > self.hitbox.y:
            y_movement = self.vel
        elif self.__destino[1] < self.hitbox.y:
            y_movement = -self.vel
        else:
            y_movement = 0

        nova_posicao = (self.hitbox.x + x_movement, self.hitbox.y + y_movement)
        self.hitbox.posicao = nova_posicao

        if self.__destino == self.hitbox.posicao:
            self.__destino = None

        self._atualizar_sprite(x_movement, y_movement)
        self.__atualizar_frente(x_movement, y_movement)

    def __atualizar_frente(self, x_movement, y_movement):
        if x_movement < 0:
            if y_movement < 0:
                self.__direction = Direction.ESQUERDA_CIMA
            elif y_movement > 0:
                self.__direction = Direction.ESQUERDA_BAIXO
            else:
                self.__direction = Direction.ESQUERDA_MEIO
        elif x_movement > 0:
            if y_movement < 0:
                self.__direction = Direction.DIREITA_CIMA
            elif y_movement > 0:
                self.__direction = Direction.DIREITA_BAIXO
            else:
                self.__direction = Direction.DIREITA_MEIO
        elif y_movement > 0:
            self.__direction = Direction.MEIO_BAIXO
        elif y_movement < 0:
            self.__direction = Direction.MEIO_CIMA

    def __calcular_distancia(self, outro_hitbox: Hitbox):
        posicao1, posicao2 = self.__determinar_posicoes_mais_proximas(outro_hitbox)

        x = abs(posicao1[0] - posicao2[0])
        y = abs(posicao1[1] - posicao2[1])

        dist = (x + y)**(1/2)
        return dist

    def __determinar_posicoes_mais_proximas(self, outro_hitbox: Hitbox):
        rect = pygame.Rect(self.hitbox.posicao, self.hitbox.tamanho)
        outro_rect = pygame.Rect(outro_hitbox.posicao, outro_hitbox.tamanho)

        if self.hitbox.x + self.hitbox.largura <= outro_hitbox.x:  # A direita
            if self.hitbox.y + self.hitbox.altura < outro_hitbox.y:  # Diagonal inferior
                return rect.bottomright, outro_rect.topleft
            elif self.hitbox.y > outro_hitbox.y + outro_hitbox.altura:  # Diagonal Superior
                return rect.topright, outro_rect.bottomleft
            else:  # Lado Direito
                return rect.midright, outro_rect.midleft

        elif self.hitbox.x >= outro_hitbox.x + outro_hitbox.largura:  # A esquerda
            if self.hitbox.y > outro_hitbox.y + outro_hitbox.altura:  # Diagonal Superior
                return rect.topleft, outro_rect.bottomright
            elif self.hitbox.y + self.hitbox.altura < outro_hitbox.y:  # Diagonal Inferior
                return rect.bottomleft, outro_rect.topright
            else:  # Lado Esquerdo
                return rect.midleft, outro_rect.midright

        elif self.hitbox.y > outro_hitbox.y:  # Acima
            return rect.midtop, outro_rect.midbottom
        else:  # Abaixo
            return rect.midbottom, outro_rect.midtop

    def __determinar_posicao_frente(self):
        rect = pygame.Rect(self.hitbox.posicao, self.hitbox.tamanho)

        if self.__direction == Direction.DIREITA_BAIXO:
            return rect.bottomright
        elif self.__direction == Direction.DIREITA_MEIO:
            return rect.midright
        elif self.__direction == Direction.DIREITA_CIMA:
            return rect.topright
        elif self.__direction == Direction.ESQUERDA_BAIXO:
            return rect.bottomleft
        elif self.__direction == Direction.ESQUERDA_MEIO:
            return rect.midleft
        elif self.__direction == Direction.ESQUERDA_CIMA:
            return rect.topleft
        elif self.__direction == Direction.MEIO_BAIXO:
            return rect.midbottom
        elif self.__direction == Direction.MEIO_CIMA:
            return rect.midtop
        else:
            return rect.midtop

    @abstractmethod
    def _calibrar_dificuldade(self):
        pass
