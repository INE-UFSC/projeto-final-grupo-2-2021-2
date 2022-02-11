from Jogador import Jogador
from Opcoes import Opcoes, Dificuldade
from TelaJogo import TelaJogo
from terrenos.Terreno2 import Terreno2
from inimigos.Inimigo1 import Inimigo1
from abstractions.AbstractFase import AbstractFase


class Fase2(AbstractFase):
    def __init__(self, jogador: Jogador, tamanho_tela: tuple, opcoes: Opcoes) -> None:
        self.__dificuldade = opcoes.dificuldade
        self.__tamanho_tela = tamanho_tela
        self.__jogador = jogador
        self.__INIMIGO_POS = []

        self.__determinar_inimigos(opcoes.dificuldade)

    @property
    def jogador(self) -> Jogador:
        return self.__jogador

    @property
    def terreno(self) -> Terreno2:
        return self.__terreno

    def load(self) -> None:
        self.__terreno = Terreno2(inimigos=[], itens=[],
                                  tamanho_tela=self.__tamanho_tela, jogador=self.__jogador)

        inimigos = []
        for x in range(len(self.__INIMIGO_POS)):
            inimigo = Inimigo1(self.__INIMIGO_POS[x], self.__dificuldade, self.__terreno)
            inimigos.append(inimigo)
        self.__terreno.load_inimigos(inimigos)

    def has_ended(self) -> bool:
        return self.__terreno.has_ended()

    def start(self, tela: TelaJogo):
        self.__jogador.terreno = self.__terreno  # Atualiza o jogador para o terreno atual
        self.__terreno.iniciar_rodada(tela, self.__jogador)

    def __determinar_inimigos(self, dificuldade: Dificuldade) -> None:
        if dificuldade == Dificuldade.facil:
            self.__INIMIGO_POS = [(200, 200), (350, 200), (900, 200),
                                  (200, 600), (1000, 600)]

        elif dificuldade == Dificuldade.medio:
            self.__INIMIGO_POS = [(200, 200), (350, 200), (900, 200),
                                  (200, 600), (400,600) , (1000, 600)]
        else:
            self.__INIMIGO_POS = [(200, 200), (350, 200), (900, 200),
                                  (200, 600), (400,600) , (1000, 600), 
                                  (150,600), (350,300)]

    def ciclo(self, tela) -> None:
        """Função para ser executada em todo ciclo do main loop"""
        for inimigo in self.__terreno.inimigos:
            inimigo.mover(self.__jogador.hitbox)
            inimigo.update()  # Em primeira instancia, vai atualizar o timer de ataque
        self.__jogador.update()  # Em primeira instancia, vai atualizar o timer de ataque
        self.__terreno.desenhar(tela, self.__jogador)
