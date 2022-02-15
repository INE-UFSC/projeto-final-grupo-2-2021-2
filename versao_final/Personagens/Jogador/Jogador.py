import pygame
from Abstractions.AbstractPersonagem import AbstractPersonagem
from Enums.Enums import Direction
from Personagens.Jogador.StatusJogador import StatusJogador


JogadorStats = {
    'vida': 10,
    'ataque': 3,
    'defesa': 2,
    'vel': 4,
    'vel_ataque': 1,
    'arma_dano': 3,
    'arma_alcance': 20
}


class Jogador(AbstractPersonagem):
    def __init__(self, posicao: tuple, tamanho: tuple, nome: str, terreno=None) -> None:
        sprite_paths = [
            "",  # Esquerda
            "",  # Direita
            "",  # Cima
            ""  # Baixo
        ]
        self.__nome = nome
        self.__status = StatusJogador(self)
        self.__direction = Direction.MEIO_CIMA

        super().__init__(stats=JogadorStats, posicao=posicao,
                         tamanho=tamanho, terreno=terreno, sprite_paths=sprite_paths)

    @property
    def status(self):
        return self.__status

    @property
    def nome(self):
        return self.__nome

    def lidar_inputs(self) -> None:
        keys = pygame.key.get_pressed()
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

    def __mover(self, keys):
        tentar_esquerda = keys[pygame.K_a]
        tentar_cima = keys[pygame.K_w]
        tentar_direita = keys[pygame.K_d]
        tentar_baixo = keys[pygame.K_s]

        self.__atualizar_frente(esquerda=tentar_esquerda,
                                direita=tentar_direita,
                                cima=tentar_cima,
                                baixo=tentar_baixo)

        # Desativa movimento horizontal caso tente ir para ambos lados
        if tentar_esquerda and tentar_direita:
            tentar_esquerda = False
            tentar_direita = False
        # Desativa movimento vertical caso tente ir para ambos lados
        if tentar_cima and tentar_baixo:
            tentar_cima = False
            tentar_baixo = False

        if tentar_esquerda:
            novo_x = self.hitbox.x - self.vel
            nova_posicao = (novo_x, self.hitbox.y)

            if self.terreno.validar_movimento(personagem=self, posicao=nova_posicao):
                self.hitbox.posicao = nova_posicao

        if tentar_direita:
            novo_x = self.hitbox.x + self.vel
            nova_posicao = (novo_x, self.hitbox.y)

            if self.terreno.validar_movimento(personagem=self, posicao=nova_posicao):
                self.hitbox.posicao = nova_posicao

        if tentar_cima:
            novo_y = self.hitbox.y - self.vel
            nova_posicao = (self.hitbox.x, novo_y)

            if self.terreno.validar_movimento(personagem=self, posicao=nova_posicao):
                self.hitbox.posicao = nova_posicao

        if tentar_baixo:
            novo_y = self.hitbox.y + self.vel
            nova_posicao = (self.hitbox.x, novo_y)

            if self.terreno.validar_movimento(personagem=self, posicao=nova_posicao):
                self.hitbox.posicao = nova_posicao

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
