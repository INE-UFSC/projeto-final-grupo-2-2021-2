from Personagens.Jogador import Jogador
from Config.Opcoes import Dificuldade
from Terrenos.DungeonMap import DungeonMap
from Personagens.Inimigos.MinotauroAzul import MinotauroAzul
from Personagens.Inimigos.MinotauroCinza import MinotauroCinza
from Personagens.Inimigos.MinotauroMarrom import MinotauroMarrom
from Personagens.Inimigos.ReaperVerde import ReaperVerde
from Fases.AbstractFase import AbstractFase


class DungeonFase(AbstractFase):
    def __init__(self, jogador: Jogador) -> None:
        super().__init__(jogador)

    def load(self) -> None:
        inimigos_quant = self.__determinar_inimigos()
        inimigos_tipos = [ReaperVerde]

        terreno = DungeonMap(enemies_quant=inimigos_quant,
                             enemies_types=inimigos_tipos,
                             jogador=self._jogador)
        super()._set_terreno(terreno)

    def __determinar_inimigos(self) -> None:
        if self._dificuldade == Dificuldade.facil:
            return 5
        elif self._dificuldade == Dificuldade.medio:
            return 7
        elif self._dificuldade == Dificuldade.dificil:
            return 10
