from Jogador import Jogador
from Opcoes import Opcoes, Dificuldade
from TelaJogo import TelaJogo
from Terreno1 import Terreno1
from Inimigo1 import Inimigo1
from abstractions.AbstractFase import AbstractFase


class Fase1(AbstractFase):
    def __init__(self, jogador: Jogador, tamanho_tela: tuple, opcoes: Opcoes) -> None:
        self.__terreno = Terreno1(inimigos=[], itens=[], tamanho_tela=tamanho_tela)
        self.__dificuldade = opcoes.dificuldade
        self.__jogador = jogador
        self.__INIMIGOS_POSICOES = []

        self.__determinar_inimigos(opcoes.dificuldade)

    @property
    def jogador(self) -> Jogador:
        return self.__jogador

    @property
    def terreno(self) -> Terreno1:
        return self.__terreno

    def load(self) -> None:
        inimigos = []
        for x in range(len(self.__INIMIGOS_POSICOES)):
            inimigos.append(Inimigo1(self.__INIMIGOS_POSICOES[x], self.__dificuldade))
        self.__terreno.load_inimigos(inimigos)

    def has_ended(self) -> bool:
        return self.__terreno.has_ended()

    def start(self, tela: TelaJogo):
        self.__terreno.iniciar_rodada(tela, self.__jogador)

    def __determinar_inimigos(self, dificuldade: Dificuldade) -> None:
        if dificuldade == Dificuldade.facil:
            self.__INIMIGOS_POSICOES = [(250, 100), (350, 50), (150, 100),
                                        (500, 50), (250, 50)]

        elif dificuldade == Dificuldade.medio:
            self.__INIMIGOS_POSICOES = [(250, 100), (350, 50), (150, 100),
                                        (500, 50), (250, 50), (250, 250)]
        else:
            self.__INIMIGOS_POSICOES = [(250, 150), (350, 50), (150, 100),
                                        (500, 50), (250, 50), (250, 100),
                                        (100, 50), (450, 50)]

    def ciclo(self, tela) -> None:
        """Função para ser executada em todo ciclo do main loop"""
        for inimigo in self.__terreno.inimigos:
            inimigo.mover(self.__jogador.hitbox)
        self.__terreno.desenhar(tela, self.__jogador)
