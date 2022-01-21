from Terreno1 import Terreno1
from abstractions.AbstractInimigo import AbstractInimigo
from Opcoes import Dificuldade


class Inimigo1(AbstractInimigo):
    def __init__(self, posicao: tuple, dificuldade: Dificuldade) -> None:
        stats = self._calibrar_dificuldade(dificuldade)
        # self.__terreno: Terreno1()
        self.__sprite_path = ""

        super().__init__(stats=stats, posicao=posicao, tamanho=(30, 30))

    @property
    def sprite_path(self) -> str:
        return self.__sprite_path

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
