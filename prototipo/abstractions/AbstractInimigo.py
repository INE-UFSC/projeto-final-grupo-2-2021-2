from abc import ABC, abstractmethod
import pygame
from Hitbox import Hitbox
from abstractions.AbstractPersonagem import AbstractPersonagem
from abstractions.AbstractTerreno import AbstractTerreno


class AbstractInimigo(AbstractPersonagem, ABC):
    def __init__(self, stats: dict, posicao: tuple, tamanho: tuple, terreno: AbstractTerreno, sprite_paths) -> None:
        super().__init__(stats, posicao, tamanho, terreno, sprite_paths)

    def mover(self, hit_jogador: Hitbox) -> None:
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

        self._atualizar_frente(esquerda=tentar_esquerda,
                               direita=tentar_direita,
                               cima=tentar_cima,
                               baixo=tentar_baixo)

    def atacar(self):
        if self.arma.atacar():
            return True
        else:
            return False

    def verificar_ataque(self, hit_jogador: Hitbox):
        distancia = self.__calcular_distancia(hit_jogador)

        if distancia < self.arma.alcance:
            return True
        else:
            return False

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

    @abstractmethod
    def _calibrar_dificuldade(self):
        pass
