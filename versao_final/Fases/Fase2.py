from Personagens.Jogador.Jogador import Jogador
from Views.Opcoes import Opcoes, Dificuldade
from Terrenos.Terreno2 import Terreno2
from Personagens.Inimigos.Inimigo2 import Inimigo2
from Abstractions.AbstractFase import AbstractFase


class Fase2(AbstractFase):
    def __init__(self, jogador: Jogador, opcoes: Opcoes) -> None:
        super().__init__(jogador, opcoes)

        self.__INIMIGO_POS = []
        self.__determinar_inimigos(opcoes.dificuldade)

    def load(self) -> None:
        self.terreno = Terreno2(inimigos=[], itens=[], jogador=self.jogador)

        inimigos = []
        for x in range(len(self.__INIMIGO_POS)):
            inimigo = Inimigo2(self.__INIMIGO_POS[x], self.dificuldade, self.terreno)
            inimigos.append(inimigo)
        self.terreno.load_inimigos(inimigos)

    def __determinar_inimigos(self, dificuldade: Dificuldade) -> None:
        if dificuldade == Dificuldade.facil:
            self.__INIMIGO_POS = [(200, 200), (350, 200), (900, 200),
                                  (200, 600), (1000, 600)]

        elif dificuldade == Dificuldade.medio:
            self.__INIMIGO_POS = [(200, 200), (350, 200), (900, 200),
                                  (200, 600), (400, 600), (1000, 600)]
        else:
            self.__INIMIGO_POS = [(200, 200), (350, 200), (900, 200),
                                  (200, 600), (400, 600), (1000, 600),
                                  (150, 600), (350, 300)]
