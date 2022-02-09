import pygame
from TelaJogo import TelaJogo
from abstractions.AbstractPersonagem import AbstractPersonagem
from abstractions.AbstractTerreno import AbstractTerreno
from obstaculos.Buraco import Buraco
from obstaculos.Parede import Parede


class Terreno1(AbstractTerreno):

    def __init__(self, inimigos: list, itens: list, tamanho_tela: tuple, jogador):
        obstaculos = []
        obstaculos.append(Parede((500, 500), (230, 10)))
        obstaculos.append(Buraco((240, 300), (10, 120)))

        sprite_path = "imagens/terreno1.png"

        super().__init__(inimigos, itens, tamanho_tela, obstaculos, jogador, sprite_path)

    def iniciar_rodada(self, tela: TelaJogo, jogador) -> None:
        # Atualiza a posição do jogador para o meio do mapa
        nova_posicao = tuple([x//2 for x in self.hitbox.tamanho])
        jogador.hitbox.posicao = nova_posicao

        self.desenhar(tela, jogador)

    def desenhar(self, tela: TelaJogo, jogador) -> None:
        mapa1 = pygame.image.load(self.sprite_path)
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

        
        cor_arma = (255,0,0)
        x_arma = jogador.hitbox.posicao[0] + jogador.hitbox.tamanho[0]
        y_arma = jogador.hitbox.posicao[1] + jogador.hitbox.tamanho[1]/4
        self.posicao_arma = (x_arma,y_arma)
        self.arma_alcance =(self.jogador.arma.alcance)
        pygame.draw.circle(tela.janela, cor_arma, self.posicao_arma, self.arma_alcance )

    def ataque(self):
        arma = pygame.Rect(self.posicao_arma, (self.arma_alcance,self.arma_alcance))
        for inimigo in self.inimigos:
            inimigo_rect = pygame.Rect(inimigo.hitbox.posicao, inimigo.hitbox.tamanho)
            if inimigo_rect.colliderect(arma):
                inimigo.vida-= self.jogador.arma.dano
                if inimigo.vida == 0:
                    self.remover_inimigo(inimigo)

    def dropar_item():
        pass

    def remover_inimigo(self,inimigo):
        self.inimigos.remove(inimigo)

    def validar_movimento(self, personagem: AbstractPersonagem, posicao: tuple) -> bool:
        if not isinstance(personagem, AbstractPersonagem):
            return False

        personagem_rect = pygame.Rect(posicao, personagem.hitbox.tamanho)
        terreno_rect = pygame.Rect(self.hitbox.posicao, self.hitbox.tamanho)
        jogador_rect = pygame.Rect(self.jogador.hitbox.posicao, self.jogador.hitbox.tamanho)

        # Validação com os cantos do terreno
        if personagem_rect.left < terreno_rect.left:
            return False
        if personagem_rect.right > terreno_rect.right:
            return False
        if personagem_rect.top < terreno_rect.top:
            return False
        if personagem_rect.bottom > terreno_rect.bottom:
            return False

        # Validação com todos os obstáculos do terreno
        for obstaculo in self.obstaculos:
            obstaculo_rect = pygame.Rect(obstaculo.hitbox.posicao, obstaculo.hitbox.tamanho)
            if personagem_rect.colliderect(obstaculo_rect):
                return False

        # Validação com os outros inimigos do terreno
        for inimigo in self.inimigos:
            if inimigo == personagem:  # Impede a comparação de uma mesma instância
                continue

            inimigo_rect = pygame.Rect(inimigo.hitbox.posicao, inimigo.hitbox.tamanho)
            if personagem_rect.colliderect(inimigo_rect):
                return False

        # Validação com o Jogador
        if personagem != self.jogador:
            if personagem_rect.colliderect(jogador_rect):
                return False

        return True

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
        
