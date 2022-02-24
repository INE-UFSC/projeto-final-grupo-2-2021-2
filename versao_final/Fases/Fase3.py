from Personagens.Jogador.Jogador import Jogador
from Config.Opcoes import Dificuldade
from Terrenos.Terreno3 import Terreno3
from Personagens.Inimigos.Inimigo3 import Inimigo3
from Abstractions.AbstractFase import AbstractFase


class Fase3(AbstractFase):
    def __init__(self, jogador: Jogador) -> None:
        super().__init__(jogador)

        self.__INIMIGO_POS = []
        self.__determinar_inimigos(self.dificuldade)

    def load(self) -> None:
        self.terreno = Terreno3(inimigos=[], itens=[], jogador=self.jogador)

        inimigos = []
        for x in range(len(self.__INIMIGO_POS)):
            inimigo = Inimigo3(self.__INIMIGO_POS[x], self.dificuldade, self.terreno)
            inimigos.append(inimigo)
        self.terreno.load_inimigos(inimigos)

    def __determinar_inimigos(self, dificuldade: Dificuldade) -> None:
        if dificuldade == Dificuldade.facil:
            self.__INIMIGO_POS = [(200, 200), (350, 200), (900, 200),
                                  (200, 600), (900, 600)]

        elif dificuldade == Dificuldade.medio:
            self.__INIMIGO_POS = [(200, 200), (350, 200), (900, 200),
                                  (200, 600), (450, 600), (900, 600)]
        else:
            self.__INIMIGO_POS = [(200, 200), (350, 200), (900, 200),
                                  (200, 600), (450, 600), (900, 600),
                                  (150, 680), (350, 300)]
