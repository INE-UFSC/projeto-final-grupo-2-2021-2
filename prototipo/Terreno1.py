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

            if inimigo.arma.desenhando_ataque:
                self.desenhar_ataque(tela, inimigo)

        if jogador.arma.desenhando_ataque:
            self.desenhar_ataque(tela, jogador)

        tamanho = jogador.hitbox.tamanho
        posicao = jogador.hitbox.posicao
        color = (0, 255, 0)
        rect = pygame.Rect(posicao, tamanho)
        pygame.draw.rect(tela.janela, color, rect)

    def dropar_item():
        pass

    def remover_inimigo(self, inimigo):
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

    def desenhar_ataque(self, tela: TelaJogo, personagem: AbstractPersonagem):
        rect_arma = personagem.rect_arma
        alcance = personagem.arma.alcance

        color = (255, 255, 255)
        pygame.draw.circle(tela.janela, color, rect_arma.center, alcance)

    def executar_ataque(self, tela: TelaJogo, personagem: AbstractPersonagem):
        self.desenhar_ataque(tela, personagem)

        rect_arma = personagem.rect_arma
        for inimigo in self.inimigos:
            rect_inimigo = pygame.Rect(inimigo.hitbox.posicao, inimigo.hitbox.tamanho)

            if rect_arma.colliderect(rect_inimigo):
                dano = personagem.dano
                dano_causado = inimigo.tomar_dano(dano)

                if inimigo.vida < 1:
                    self.remover_inimigo(inimigo)

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
