from abstractions.AbstractInimigo import AbstractInimigo
from Opcoes import Dificuldade
from abstractions.AbstractTerreno import AbstractTerreno


class Inimigo1(AbstractInimigo):
    def __init__(self, posicao: tuple, dificuldade: Dificuldade, terreno: AbstractTerreno) -> None:
        stats = self._calibrar_dificuldade(dificuldade)
        sprite_paths = [
            "",  # Esquerda
            "",  # Direita
            "",  # Cima
            ""  # Baixo
        ]

        super().__init__(stats=stats, posicao=posicao, tamanho=(30, 30),
                         terreno=terreno, sprite_paths=sprite_paths)

    def _calibrar_dificuldade(self, dificuldade: Dificuldade) -> dict:
        if dificuldade.medio:
            return {
                'vida': 7, 'ataque': 5, 'defesa': 2,
                'vel': 2, 'vel_ataque': 1, 'arma_dano': 2,
                'arma_alcance': 2
            }
        elif dificuldade.dificil:
            return {
                'vida': 10, 'ataque': 6, 'defesa': 3,
                'vel': 2, 'vel_ataque': 1, 'arma_dano': 4,
                'arma_alcance': 2
            }
        else:  # Facil
            return {
                'vida': 5, 'ataque': 4, 'defesa': 1,
                'vel': 2, 'vel_ataque': 1, 'arma_dano': 1,
                'arma_alcance': 1
            }

    def atacar():
        pass
