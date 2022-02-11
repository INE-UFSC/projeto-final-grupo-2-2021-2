from abstractions.AbstractPersonagem import AbstractPersonagem
import pygame

class StatusJogador():

    """Formata as informações do jogador para aparecer na tela"""
    def __init__(self, jogador: AbstractPersonagem) -> None:
        self.__jogador = jogador

    def vida(self):
        """Irá lidar com o retorno dos sprites para representar a vida"""
        fonte = pygame.font.SysFont('arial', 40, False, False)
        texto_formatado = fonte.render(f'Vida: {self.Jogador.vida}', True, (255,255,255))
        return texto_formatado

    def arma():
        """Irá lidar com o retorno dos sprites para representar a arma"""
        pass
