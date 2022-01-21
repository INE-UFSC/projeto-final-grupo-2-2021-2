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
    'arma_alcance': 3
}


class Jogador(AbstractPersonagem):
    def __init__(self, posicao: tuple, tamanho: tuple, nome: str) -> None:
        super().__init__(stats=JogadorStats, posicao=posicao, tamanho=tamanho)
        self.__nome = nome
        self.__status = StatusJogador(self)
        self.__sprite_path = ""

    @property
    def status(self):
        return self.__status

    @property
    def sprite_path(self) -> str:
        return self.__sprite_path

    @property
    def nome(self):
        return self.__nome

    def lidar_inputs(self, keys) -> None:
        self.__mover(keys)

    def __mover(self, keys):
        if keys[pygame.K_a]:
            novo_x = self.hitbox.x - self.vel
            nova_posicao = (novo_x, self.hitbox.y)
            # Validar
            if True:
                self.hitbox.posicao = nova_posicao

        if keys[pygame.K_d]:
            novo_x = self.hitbox.x + self.vel
            nova_posicao = (novo_x, self.hitbox.y)
            if True:
                self.hitbox.posicao = nova_posicao

        if keys[pygame.K_w]:
            novo_y = self.hitbox.y - self.vel
            nova_posicao = (self.hitbox.x, novo_y)
            if True:
                self.hitbox.posicao = nova_posicao

        if keys[pygame.K_s]:
            novo_y = self.hitbox.y + self.vel
            nova_posicao = (self.hitbox.x, novo_y)
            if True:
                self.hitbox.posicao = nova_posicao

    def atacar():
        pass

    def mover():
        pass
