from Terrenos.terrenos import matriz_terreno3
from Abstractions.AbstractTerreno import AbstractTerreno


class Terreno3(AbstractTerreno):

    def __init__(self, inimigos: list, itens: list, jogador):
        sprite_path = "imagens/terreno1.png"

        super().__init__(inimigos, itens, jogador, sprite_path)
        super()._setup_mapa(matriz_terreno3)

    def has_ended(self) -> bool:
        for inimigo in self.inimigos:
            if not inimigo.morreu:
                return False
        return True
