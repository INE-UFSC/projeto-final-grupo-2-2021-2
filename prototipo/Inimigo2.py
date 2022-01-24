from Opcoes import Dificuldade
from abstractions.AbstractInimigo import AbstractInimigo
from abstractions.AbstractPersonagem import AbstractPersonagem
from abstractions.AbstractTerreno import AbstractTerreno
from stats import Inimigo2Stats


class Inimigo2(AbstractInimigo):
    def __init__(self, posicao: tuple, dificuldade: Dificuldade, terreno: AbstractTerreno) -> None:
        sprite_paths = [
            "",  # Esquerda
            "",  # Direita
            "",  # Cima
            ""  # Baixo
        ]

        super().__init__(stats=Inimigo2Stats, posicao=posicao,
                         tamanho=(6, 6), terreno=terreno, sprite_paths=sprite_paths)
