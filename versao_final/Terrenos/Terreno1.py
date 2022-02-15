from Terrenos.terrenos import matriz_terreno1
from Abstractions.AbstractTerreno import AbstractTerreno


class Terreno1(AbstractTerreno):

    def __init__(self, inimigos: list, itens: list, jogador):
        sprite_path = "imagens/terreno1.png"

        super().__init__(inimigos, itens, jogador, sprite_path)
        super()._setup_mapa(matriz_terreno1)

    def dropar_item():
        pass

    def has_ended(self) -> bool:
        for inimigo in self.inimigos:
            if inimigo.vida > 0:
                return False
        return True
