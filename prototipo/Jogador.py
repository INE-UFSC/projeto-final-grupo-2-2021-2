import pygame
from abstractions.AbstractPersonagem import AbstractPersonagem
from StatusJogador import StatusJogador


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

    def __mover(self, keys):
        tentar_esquerda = keys[pygame.K_a]
        tentar_cima = keys[pygame.K_w]
        tentar_direita = keys[pygame.K_d]
        tentar_baixo = keys[pygame.K_s]

        self._atualizar_frente(esquerda=tentar_esquerda,
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
