from AbstractPersonagem import AbstractPersonagem
from StatusJogador import StatusJogador
from stats import JogadorStats


class Jogador(AbstractPersonagem):
    def __init__(self, posicao: tuple, tamanho: tuple, nome: str) -> None:
        super().__init__(stats=JogadorStats, posicao=posicao, tamanho=tamanho)
        self.__nome = nome
        self.__status = StatusJogador(self)

    @property
    def status(self):
        return self.__status

    @property
    def nome(self):
        return self.__nome

    def mover(self, key) -> tuple:
        # Determinar qual a direção que o jogador escolheu
        # Validar com o terreno se a nova posição é valida
        # Se sim, atualizá-la
        pass
