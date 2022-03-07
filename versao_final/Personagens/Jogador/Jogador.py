from typing import List
import pygame
from Abstractions.AbstractPersonagem import AbstractPersonagem
from Abstractions.AbstractItem import AbstractItem
from Enums.Enums import Direction
from Utils.Folder import import_folder


class Jogador(AbstractPersonagem):
    __BASE_PATH = 'Assets/Player/{}/{}'
    __ANIMACOES_IMPORTADAS = False
    __IMAGE_SIZE = (60, 65)
    __STATS = {
        'vida': 30,
        'ataque': 5,
        'defesa': 5,
        'vel': 3,
        'vel_ataque': 1,
        'arma_dano': 3,
        'arma_alcance': 17,
        'transpassavel': False
    }

    def __init__(self, posicao: tuple, nome: str, terreno=None) -> None:
        self.__itens: List[AbstractItem] = []
        self.__nome = nome

        super().__init__(stats=Jogador.__STATS, posicao=posicao, tamanho=(30, 48), terreno=terreno)

        self.__direction = Direction.MEIO_CIMA

        if not Jogador.__ANIMACOES_IMPORTADAS:
            Jogador.__import_character_assets()
            Jogador.__ANIMACOES_IMPORTADAS = True

        self.__str_direction = self.__Direction_to_str_direction(self.__direction)

        self.__animation = 'Idle'
        self.__frame_index = 0
        self.__animation_speed = 0.30
        self.__LAST_ANIMATION = 'Idle'
        self.__ANIMACAO_RESETADA = False
        self.__FRAME_TO_WAIT = 0
        self.__MORREU = False

        self.__animations = Jogador.__animations[self.__animation][self.__str_direction]
        self.__image = self.image
        self.__rect = self.rect

    @property
    def image(self) -> pygame.Surface:
        if int(self.__frame_index) >= self.__animations_length[self.__animation]:
            self.__frame_index = 0

        self.__str_direction = self.__Direction_to_str_direction(self.__direction)
        self.__image = Jogador.__animations[self.__animation][self.__str_direction][int(
            self.__frame_index)]
        return self.__image

    @property
    def rect(self) -> pygame.Rect:
        x_for_image = self.hitbox.center[0]
        y_for_image = self.hitbox.center[1] - int(self.hitbox.tamanho[1] * 0.2)
        self.__rect = self.__image.get_rect(center=(x_for_image, y_for_image))
        return self.__rect

    def lidar_inputs(self) -> None:
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
            self.terreno.pegar_item()
        if keys[pygame.K_j]:
            if self.__atacar():
                self.__set_animation('Attacking')
        if keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_d]:
            self.__mover(keys)
            self.__set_animation('Walking')
        else:
            self.__set_animation('Idle')

    def animate(self) -> None:
        animation_name = self.__animation
        direction_str = self.__Direction_to_str_direction(self.__direction)
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

    def atacar(self) -> bool:
        if self.__animation != 'Attacking':
            return False

        if self.__frame_index > 5 and self.__frame_index < 5 + self.__animation_speed:
            return True
        else:
            return False

    @property
    def direction(self) -> Direction:
        return self.__direction

    def __atacar(self) -> bool:
        if self.__animation == 'Attacking' or self.__animation == 'Dying':
            return False
        else:
            if self.arma.atacar():
                return True
            else:
                return False

    def get_rect_arma(self) -> pygame.Rect:
        posicao_frente = self.__posicao_frente()

        rect = pygame.Rect(posicao_frente, (self.alcance, self.alcance))
        rect.center = posicao_frente
        return rect

    def receber_item(self, item: AbstractItem) -> None:
        self.__itens.append(item)
        item.modificar_status(self.status)

    def update(self) -> None:
        self.arma.update()
        for item in self.__itens:
            if item.check_aplicado():
                self.__itens.remove(item)

    def __atualizar_frente(self, x_movement, y_movement):
        if x_movement < 0:
            if y_movement < 0:
                self.__direction = Direction.ESQUERDA_CIMA
            elif y_movement > 0:
                self.__direction = Direction.ESQUERDA_BAIXO
            else:
                self.__direction = Direction.ESQUERDA_MEIO
        elif x_movement > 0:
            if y_movement < 0:
                self.__direction = Direction.DIREITA_CIMA
            elif y_movement > 0:
                self.__direction = Direction.DIREITA_BAIXO
            else:
                self.__direction = Direction.DIREITA_MEIO
        elif y_movement > 0:
            self.__direction = Direction.MEIO_BAIXO
        elif y_movement < 0:
            self.__direction = Direction.MEIO_CIMA

    def __Direction_to_str_direction(self, direction: Direction) -> str:
        if direction == Direction.ESQUERDA_CIMA:
            return 'Esquerda'
        elif direction == Direction.ESQUERDA_MEIO:
            return 'Esquerda'
        elif direction == Direction.ESQUERDA_MEIO:
            return 'Esquerda'
        elif direction == Direction.ESQUERDA_BAIXO:
            return 'Esquerda'
        elif direction == Direction.DIREITA_BAIXO:
            return 'Direita'
        elif direction == Direction.DIREITA_MEIO:
            return 'Direita'
        elif direction == Direction.DIREITA_CIMA:
            return 'Direita'
        elif direction == Direction.MEIO_CIMA:
            return 'Cima'
        elif direction == Direction.MEIO_BAIXO:
            return 'Baixo'

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
            if self.terreno.validar_movimento(personagem=self, posicao=nova_posicao_x):
                self.hitbox.posicao = nova_posicao_x

        if y_movement != 0:
            nova_posicao_y = (self.hitbox.x, self.hitbox.y + y_movement)
            if self.terreno.validar_movimento(personagem=self, posicao=nova_posicao_y):
                self.hitbox.posicao = nova_posicao_y

        self.__atualizar_frente(x_movement, y_movement)

    def __posicao_frente(self):
        rect = pygame.Rect(self.hitbox.posicao, self.hitbox.tamanho)

        if self.__direction == Direction.DIREITA_BAIXO:
            return rect.bottomright
        elif self.__direction == Direction.DIREITA_MEIO:
            return rect.midright
        elif self.__direction == Direction.DIREITA_CIMA:
            return rect.topright
        elif self.__direction == Direction.ESQUERDA_BAIXO:
            return rect.bottomleft
        elif self.__direction == Direction.ESQUERDA_MEIO:
            return rect.midleft
        elif self.__direction == Direction.ESQUERDA_CIMA:
            return rect.topleft
        elif self.__direction == Direction.MEIO_BAIXO:
            return rect.midbottom
        elif self.__direction == Direction.MEIO_CIMA:
            return rect.midtop
        else:
            return rect.midtop

    @property
    def morreu(self) -> bool:
        return self.__MORREU

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
