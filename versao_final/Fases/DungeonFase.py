from Personagens.Jogador import Jogador
from Config.Opcoes import Dificuldade
from Terrenos.DungeonMap import DungeonMap
from Personagens.Inimigos.Minotauro import Minotauro
from Fases.AbstractFase import AbstractFase


class DungeonFase(AbstractFase):
    def __init__(self, jogador: Jogador) -> None:
        super().__init__(jogador)

    def load(self) -> None:
        inimigos_quant = self.__determinar_inimigos()
        inimigos_tipos = [Minotauro]

        terreno = DungeonMap(enemies_quant=inimigos_quant,
                             enemies_types=inimigos_tipos,
                             jogador=self._jogador)
        super()._set_terreno(terreno)

    def __determinar_inimigos(self) -> None:
        if self._dificuldade == Dificuldade.facil:
            return 5
        elif self._dificuldade == Dificuldade.medio:
            return 3
        elif self._dificuldade == Dificuldade.dificil:
            return 10
