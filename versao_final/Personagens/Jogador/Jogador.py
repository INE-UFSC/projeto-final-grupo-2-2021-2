from typing import List
import pygame
from Abstractions.AbstractPersonagem import AbstractPersonagem
from Abstractions.AbstractItem import AbstractItem
from Enums.Enums import Direction


class Jogador(AbstractPersonagem):
    __STATS = {
        'vida': 30,
        'ataque': 5,
        'defesa': 5,
        'vel': 3,
        'vel_ataque': 1,
        'arma_dano': 3,
        'arma_alcance': 17,
        'transpassavel': False
    }

    def __init__(self, posicao: tuple, tamanho: tuple, nome: str, terreno=None) -> None:
        self.__itens: List[AbstractItem] = []
        self.__nome = nome
        self.__direction = Direction.MEIO_CIMA

        super().__init__(stats=Jogador.__STATS, posicao=posicao, tamanho=tamanho, terreno=terreno)

    @property
    def direction(self) -> Direction:
        return self.__direction

    def lidar_inputs(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.terreno.pegar_item()

        self.__mover(keys)

    def verificar_ataque(self) -> bool:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_j]:
            return self.atacar()
        else:
            return False

    def atacar(self) -> bool:
        if self.arma.atacar():
            return True
        else:
            return False

    def get_rect_arma(self) -> pygame.Rect:
        posicao_frente = self.__posicao_frente()

        rect = pygame.Rect(posicao_frente, (self.alcance, self.alcance))
        rect.center = posicao_frente
        return rect

    def receber_item(self, item: AbstractItem) -> None:
        self.__itens.append(item)
        item.modificar_status(self.status)

    def update(self) -> None:
        self.arma.update()
        for item in self.__itens:
            if item.check_aplicado():
                self.__itens.remove(item)

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

    def __mover(self, keys):
        tentar_esquerda = keys[pygame.K_a]
        tentar_cima = keys[pygame.K_w]
        tentar_direita = keys[pygame.K_d]
        tentar_baixo = keys[pygame.K_s]

        # Desativa movimento horizontal caso tente ir para ambos lados
        if tentar_esquerda and tentar_direita:
            tentar_esquerda = False
            tentar_direita = False
        # Desativa movimento vertical caso tente ir para ambos lados
        if tentar_cima and tentar_baixo:
            tentar_cima = False
            tentar_baixo = False

        if tentar_esquerda:
            x_movement = - self.vel
        elif tentar_direita:
            x_movement = self.vel
        else:
            x_movement = 0

        if tentar_cima:
            y_movement = - self.vel
        elif tentar_baixo:
            y_movement = self.vel
        else:
            y_movement = 0

        if x_movement != 0:
            nova_posicao_x = (self.hitbox.x + x_movement, self.hitbox.y)
            if self.terreno.validar_movimento(personagem=self, posicao=nova_posicao_x):
                self.hitbox.posicao = nova_posicao_x

        if y_movement != 0:
            nova_posicao_y = (self.hitbox.x, self.hitbox.y + y_movement)
            if self.terreno.validar_movimento(personagem=self, posicao=nova_posicao_y):
                self.hitbox.posicao = nova_posicao_y

        self.__atualizar_frente(x_movement, y_movement)

    def __posicao_frente(self):
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
