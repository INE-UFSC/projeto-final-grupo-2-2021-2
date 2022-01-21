import pygame
from TelaJogo import TelaJogo
from abstractions.AbstractTerreno import AbstractTerreno
from obstaculos.Buraco import Buraco
from obstaculos.Parede import Parede


class Terreno1(AbstractTerreno):

    def __init__(self, inimigos: list, itens: list, tamanho_tela: tuple):
        obstaculos = []
        obstaculos.append(Parede((500, 500), (230, 10)))
        obstaculos.append(Buraco((240, 300), (10, 120)))

        super().__init__(inimigos, itens, tamanho_tela, obstaculos)
        self.__sprite_path = "imagens/terreno1.png"

    @property
    def sprite_path(self) -> str:
        return self.__sprite_path

    def iniciar_rodada(self, tela: TelaJogo, jogador) -> None:
        # Atualiza a posição do jogador para o meio do mapa
        nova_posicao = tuple([x//2 for x in self.hitbox.tamanho])
        jogador.hitbox.posicao = nova_posicao

        self.desenhar(tela, jogador)

    def desenhar(self, tela: TelaJogo, jogador) -> None:
        mapa1 = pygame.image.load(self.__sprite_path)
        tela.janela.blit(mapa1, (0, 0))
        for obstaculo in self.obstaculos:
            posicao = obstaculo.hitbox.posicao
            tamanho = obstaculo.hitbox.tamanho
            color = (0, 0, 0)
            rect = pygame.Rect(posicao, tamanho)
            pygame.draw.rect(tela.janela, color, rect)

        for inimigo in self.inimigos:
            posicao = inimigo.hitbox.posicao
            tamanho = inimigo.hitbox.tamanho
            color = (0, 0, 125)
            rect = pygame.Rect(posicao, tamanho)
            pygame.draw.rect(tela.janela, color, rect)

        tamanho = jogador.hitbox.tamanho
        posicao = jogador.hitbox.posicao
        color = (0, 255, 0)
        rect = pygame.Rect(posicao, tamanho)
        pygame.draw.rect(tela.janela, color, rect)

    def dropar_item():
        pass

    def remover_inimigo():
        pass

    def validar_movimento():
        pass

    def load_inimigos(self, inimigos: list) -> None:
        self.inimigos.extend(inimigos)

    def has_ended(self) -> bool:
        for inimigo in self.inimigos:
            if inimigo.vida > 0:
                return False
        return True

    def mover_inimigos(self) -> None:
        for inimigo in self.inimigos:
            inimigo.mover()
