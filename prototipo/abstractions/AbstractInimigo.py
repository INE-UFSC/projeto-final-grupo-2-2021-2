from abc import ABC, abstractmethod
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

        if hit_jogador.x > self.hitbox.x:
            novo_x = self.hitbox.x + self.vel
            tentar_direita = True
        else:
            novo_x = self.hitbox.x - self.vel
            tentar_esquerda = True

        nova_posicao = (novo_x, self.hitbox.y)

        if self.terreno.validar_movimento(personagem=self, posicao=nova_posicao):
            self.hitbox.posicao = nova_posicao

        if hit_jogador.y > self.hitbox.y:
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

    @abstractmethod
    def _calibrar_dificuldade(self):
        pass

    def update(self):
        pass
