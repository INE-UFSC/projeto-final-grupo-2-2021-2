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

    def update(self, hit_jogador: Hitbox):
        if self.__em_repouso:
            if self.__esta_vendo_jogador(hit_jogador):
                self.__em_repouso = False
        super().update()

    def mover(self, hit_jogador: Hitbox) -> None:
        if self.__em_repouso:
            return None

        if self.__destino != None:
            self.__mover_destino()
            return
        else:
            destino = self.terreno.get_destino(self.hitbox.posicao, hit_jogador.posicao)
            if destino != None:
                self.__destino = destino
                self.__mover_destino()
                return

        tentar_esquerda = False
        tentar_direita = False
        tentar_cima = False
        tentar_baixo = False

        rect_jogador = pygame.Rect(hit_jogador.posicao, hit_jogador.tamanho)
        center_jogador = rect_jogador.center

        if center_jogador[0] > self.hitbox.x:
            novo_x = self.hitbox.x + self.vel
            tentar_direita = True
        else:
            novo_x = self.hitbox.x - self.vel
            tentar_esquerda = True

        nova_posicao = (novo_x, self.hitbox.y)

        if self.terreno.validar_movimento(personagem=self, posicao=nova_posicao):
            self.hitbox.posicao = nova_posicao

        if center_jogador[1] > self.hitbox.y:
            novo_y = self.hitbox.y + self.vel
            tentar_baixo = True
        else:
            novo_y = self.hitbox.y - self.vel
            tentar_cima = True

        nova_posicao = (self.hitbox.x, novo_y)
        if self.terreno.validar_movimento(personagem=self, posicao=nova_posicao):
            self.hitbox.posicao = nova_posicao

        self._atualizar_sprite(esquerda=tentar_esquerda,
                               direita=tentar_direita,
                               cima=tentar_cima,
                               baixo=tentar_baixo)

        self.__atualizar_frente(esquerda=tentar_esquerda,
                                direita=tentar_direita,
                                cima=tentar_cima,
                                baixo=tentar_baixo)

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

    def __atualizar_frente(self, esquerda, direita, cima, baixo):
        if esquerda:
            if cima:
                self.__direction = Direction.ESQUERDA_CIMA
            elif baixo:
                self.__direction = Direction.ESQUERDA_BAIXO
            else:
                self.__direction = Direction.ESQUERDA_MEIO
        elif direita:
            if cima:
                self.__direction = Direction.DIREITA_CIMA
            elif baixo:
                self.__direction = Direction.DIREITA_BAIXO
            else:
                self.__direction = Direction.DIREITA_MEIO
        elif baixo:
            self.__direction = Direction.MEIO_BAIXO
        elif cima:
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
