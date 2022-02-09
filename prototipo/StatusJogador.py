from abstractions.AbstractPersonagem import AbstractPersonagem
import pygame
class StatusJogador():
    """Formata as informações do jogador para aparecer na tela"""

    def __init__(self, jogador: AbstractPersonagem) -> None:
        self.__jogador = jogador

    def vida():
        """Irá lidar com o retorno dos sprites para representar a vida"""
        font = pygame.font.Font(None, 40)
        distancia_imagem = font.render(f'Vida:{Jogador.JogadorStats}', False, (142,0,28))
        distancia_rect = distancia_imagem.get_rect(center = (400, 100))
        return pygame.screen.blit(distancia_imagem, distancia_rect)

    def arma():
        """Irá lidar com o retorno dos sprites para representar a arma"""
        pass
    
    
    
    
    def tela_de_distancia():
        statusvida = int(pygame.time.get_ticks()/2000) - 0
        distancia_imagem = pygame.font.render(f'Distância:{statusvida}', False, (142,0,28))
        distancia_rect = distancia_imagem.get_rect(center = (400, 100))
        pygame.screen.blit(distancia_imagem, distancia_rect)
        return statusvida