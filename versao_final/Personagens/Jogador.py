from typing import List
import pygame
from Personagens.AbstractPersonagem import AbstractPersonagem
from Itens.AbstractItem import AbstractItem
from Config.Enums import Direction
from Utils.Folder import import_folder


class Jogador(AbstractPersonagem):
    __BASE_PATH = 'Assets/Player/{}/{}'
    __ANIMACOES_IMPORTADAS = False
    __IMAGE_SIZE = (60, 65)
    __STATS = {
        'vida': 50,
        'ataque': 5,
        'defesa': 5,
        'vel': 3,
        'vel_ataque': 1,
        'arma_dano': 3,
        'arma_alcance': 20,
        'transpassavel': False
    }

    def __init__(self, posicao: tuple, nome: str, mapa=None) -> None:
        self.__itens: List[AbstractItem] = []
        self.__nome = nome

        super().__init__(stats=Jogador.__STATS, posicao=posicao, tamanho=(30, 48), mapa=mapa)

        if not Jogador.__ANIMACOES_IMPORTADAS:
            Jogador.__import_character_assets()
            Jogador.__ANIMACOES_IMPORTADAS = True

        self.__animation = 'Idle'
        self.__frame_index = 0
        self.__animation_speed = 0.30
        self.__LAST_ANIMATION = 'Idle'
        self.__ANIMACAO_RESETADA = False
        self.__FRAME_TO_WAIT = 0
        self.__MORREU = False
        self.__ACABOU_DE_TOMAR_DANO = False

        self.__str_direction = self.__get_direction_sprites()
        self.__animations = Jogador.__animations[self.__animation][self.__str_direction]
        self.__image = self.image
        self.__rect = self.rect

    def processar_inputs(self) -> None:
        keys = pygame.key.get_pressed()
        if self.vida <= 0:
            if self.__animation != 'Dying':
                self.__set_animation('Dying')

            if self.__FRAME_TO_WAIT > 0:
                self.__FRAME_TO_WAIT -= 1
                return None
            else:
                self.__MORREU = True
            return None

        if keys[pygame.K_e]:
            self.mapa.pegar_item()
        if keys[pygame.K_j]:
            if self.__atacar():
                self.__set_animation('Attacking')
        if keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_d]:
            self.__mover(keys)
            self.__set_animation('Walking')
        else:
            self.__set_animation('Idle')

    def atacar(self) -> bool:
        if self.__animation != 'Attacking':
            return False

        if self.__frame_index > 5 and self.__frame_index < 5 + self.__animation_speed:
            return True
        else:
            return False

    def tomar_dano(self, dano: int) -> int:
        if type(dano) == int:
            dano_real = dano - self.status.defesa
            if dano_real > 0:
                self.status.vida -= dano_real
                return dano_real
            else:
                return 0
        else:
            return 0

    def pontos_para_ataque(self) -> list:
        return super().pontos_para_ataque()

    def receber_item(self, item: AbstractItem) -> None:
        self.__itens.append(item)
        item.modificar_status(self.status)

    def update(self) -> None:
        for item in self.__itens:
            if item.check_aplicado():
                self.__itens.remove(item)

    @classmethod
    def __import_character_assets(cls):
        cls.__animations = {}
        cls.__animations_length = {}
        animations_names = ['Walking', 'Attacking', 'Idle', 'Dying']
        directions_names = ['Cima', 'Direita', 'Baixo', 'Esquerda']

        for animation in animations_names:
            directions = {}
            for direction in directions_names:
                full_path = cls.__BASE_PATH.format(animation, direction)
                images = import_folder(full_path, cls.__IMAGE_SIZE)
                directions[direction] = images

            cls.__animations[animation] = directions
            cls.__animations_length[animation] = len(directions['Cima'])

    @property
    def image(self) -> pygame.Surface:
        if int(self.__frame_index) >= self.__animations_length[self.__animation]:
            self.__frame_index = 0

        self.__str_direction = self.__get_direction_sprites()
        animations = Jogador.__animations[self.__animation]
        self.__image = animations[self.__str_direction][int(self.__frame_index)]
        return self.__image

    @property
    def rect(self) -> pygame.Rect:
        x_for_image = self.hitbox.center[0]
        y_for_image = self.hitbox.center[1] - int(self.hitbox.tamanho[1] * 0.2)
        self.__rect = self.__image.get_rect(center=(x_for_image, y_for_image))
        return self.__rect

    def animate(self) -> None:
        animation_name = self.__animation
        direction_str = self.__get_direction_sprites()
        animations = Jogador.__animations[animation_name][direction_str]

        if self.__ANIMACAO_RESETADA:
            self.__ANIMACAO_RESETADA = False

        if self.__LAST_ANIMATION != animation_name:
            self.__frame_index = 0
        self.__LAST_ANIMATION = animation_name

        self.__frame_index += self.__animation_speed
        if self.__frame_index >= len(animations):
            self.__frame_index = 0
            self.__ANIMACAO_RESETADA = True

    @property
    def morreu(self) -> bool:
        return self.__MORREU

    def __atacar(self) -> bool:
        if self.__animation == 'Attacking' or self.__animation == 'Dying':
            return False
        else:
            return True

    def __set_animation(self, animation: str) -> None:
        # Animação não pode ser sobreposta
        if self.__animation == 'Dying':
            return None

        if self.__FRAME_TO_WAIT > 0:
            self.__FRAME_TO_WAIT -= 1
            return None

        if animation == 'Attacking':
            self.__animation = animation
            self.__set_animation_frame_to_wait(animation)

        if animation == 'Dying':
            self.__animation = animation
            self.__set_animation_frame_to_wait(animation)

        if animation == 'Walking':
            self.__animation = animation

        if animation == 'Idle':
            self.__animation = animation

    def __set_animation_frame_to_wait(self, animation: str) -> None:
        self.__FRAME_TO_WAIT = Jogador.__animations_length[animation] // self.__animation_speed

    def __get_direction_sprites(self) -> str:
        if self.direction == Direction.ESQUERDA_CIMA:
            return 'Esquerda'
        elif self.direction == Direction.ESQUERDA_MEIO:
            return 'Esquerda'
        elif self.direction == Direction.ESQUERDA_BAIXO:
            return 'Esquerda'
        elif self.direction == Direction.DIREITA_BAIXO:
            return 'Direita'
        elif self.direction == Direction.DIREITA_MEIO:
            return 'Direita'
        elif self.direction == Direction.DIREITA_CIMA:
            return 'Direita'
        elif self.direction == Direction.MEIO_CIMA:
            return 'Cima'
        elif self.direction == Direction.MEIO_BAIXO:
            return 'Baixo'
        else:
            return 'Cima'

    def __mover(self, keys) -> None:
        if self.__animation == 'Attacking' or self.__animation == 'Dying':
            return None

        tentar_esquerda = keys[pygame.K_a]
        tentar_cima = keys[pygame.K_w]
        tentar_direita = keys[pygame.K_d]
        tentar_baixo = keys[pygame.K_s]

        # Desativa movimento horizontal caso tente ir para ambos lados
        if tentar_esquerda and tentar_direita:
            tentar_esquerda = False
            tentar_direita = False
        # Desativa movimento vertical caso tente ir para ambos lados
        if tentar_cima and tentar_baixo:
            tentar_cima = False
            tentar_baixo = False

        if tentar_esquerda:
            x_movement = - self.vel
        elif tentar_direita:
            x_movement = self.vel
        else:
            x_movement = 0

        if tentar_cima:
            y_movement = - self.vel
        elif tentar_baixo:
            y_movement = self.vel
        else:
            y_movement = 0

        if x_movement != 0:
            nova_posicao_x = (self.hitbox.x + x_movement, self.hitbox.y)
            if self.mapa.validar_movimento(personagem=self, posicao=nova_posicao_x):
                self.hitbox.posicao = nova_posicao_x

        if y_movement != 0:
            nova_posicao_y = (self.hitbox.x, self.hitbox.y + y_movement)
            if self.mapa.validar_movimento(personagem=self, posicao=nova_posicao_y):
                self.hitbox.posicao = nova_posicao_y

        self._atualizar_frente(x_movement, y_movement)
