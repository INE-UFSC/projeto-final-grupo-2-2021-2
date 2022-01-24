from Opcoes import Dificuldade
from abstractions.AbstractInimigo import AbstractInimigo
from abstractions.AbstractTerreno import AbstractTerreno
from stats import Inimigo3Stats


class Inimigo3(AbstractInimigo):
    def __init__(self, posicao: tuple, dificuldade: Dificuldade, terreno: AbstractTerreno) -> None:
        sprite_paths = [
            "",  # Esquerda
            "",  # Direita
            "",  # Cima
            ""  # Baixo
        ]

        super().__init__(stats=Inimigo3Stats, posicao=posicao,
                         tamanho=(3, 3), terreno=terreno, sprite_paths=sprite_paths)
