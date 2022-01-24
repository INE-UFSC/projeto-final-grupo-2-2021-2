from abc import ABC, abstractmethod
from Hitbox import Hitbox
from abstractions.AbstractPersonagem import AbstractPersonagem
from abstractions.AbstractTerreno import AbstractTerreno


class AbstractInimigo(AbstractPersonagem, ABC):
    def __init__(self, stats: dict, posicao: tuple, tamanho: tuple, terreno: AbstractTerreno) -> None:
        super().__init__(stats, posicao, tamanho, terreno)

    def mover(self, hit_jogador: Hitbox) -> None:
        if hit_jogador.x > self.hitbox.x:
            novo_x = self.hitbox.x + self.vel
        else:
            novo_x = self.hitbox.x - self.vel

        nova_posicao = (novo_x, self.hitbox.y)
        self.terreno.validar_movimento()
        if True:
            self.hitbox.posicao = nova_posicao

        if hit_jogador.y > self.hitbox.y:
            novo_y = self.hitbox.y + self.vel
        else:
            novo_y = self.hitbox.y - self.vel

        nova_posicao = (self.hitbox.x, novo_y)
        self.terreno.validar_movimento()
        if True:
            self.hitbox.posicao = nova_posicao

    @property
    @abstractmethod
    def sprite_path(self) -> str:
        pass

    @abstractmethod
    def _calibrar_dificuldade(self):
        pass
