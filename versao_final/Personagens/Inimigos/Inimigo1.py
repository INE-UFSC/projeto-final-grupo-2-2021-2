from Enums.Enums import Dificuldade, Direction, Estado
from Abstractions.AbstractInimigo import AbstractInimigo
from Abstractions.AbstractTerreno import AbstractTerreno
from Utils.Folder import import_fliped_folder, import_folder
from Utils.Hitbox import Hitbox
from random import random
from pygame import sprite, Surface, Rect


class Inimigo1(AbstractInimigo, sprite.Sprite):
    def __init__(self, posicao: tuple, dificuldade: Dificuldade, terreno: AbstractTerreno) -> None:
        stats = self._calibrar_dificuldade(dificuldade)
        sprite_paths = [
            "",  # Esquerda
            "",  # Direita
            "",  # Cima
            ""  # Baixo
        ]
        super().__init__(stats=stats, posicao=posicao, tamanho=(36, 48),
                         terreno=terreno, sprite_paths=sprite_paths)
        self.__animation = 'Idle'
        self.__tamanho_imagem = (80, 65)
        self.__frame_index = 0
        self.__animation_speed = 0.35
        self.__FRAME_TO_WAIT = 0
        self.__MORREU = False
        self.__LAST_ANIMATION = 'Idle'
        self.__CHANCE_DAMAGE_STOP_ATTACK = 0.6
        self.__ANIMACAO_RESETADA = False
        self.__import_character_assets()

    @property
    def image(self) -> Surface:
        if self.__frame_index >= len(self.__animations[self.__animation]):
            self.__frame_index = 0

        self.__image = self.__animations[self.__animation][int(self.__frame_index)]
        return self.__image

    @property
    def rect(self) -> Rect:
        self.__rect = self.__image.get_rect(center=self.hitbox.center)
        return self.__rect

    def animate(self) -> None:
        animation_name = self.__get_current_animation()
        animation = self.__animations[animation_name]

        if self.__ANIMACAO_RESETADA:
            self.__ANIMACAO_RESETADA = False

        # Reseta o frame index caso tenha trocado a animação
        if self.__LAST_ANIMATION != animation_name:
            self.__frame_index = 0
        self.__LAST_ANIMATION = animation_name

        self.__frame_index += self.__animation_speed
        if self.__frame_index >= len(animation):
            self.__frame_index = 0
            self.__ANIMACAO_RESETADA = True

    def mover(self, *args) -> None:
        # Se está atacando ou tomou dano não vai andar até a animação terminar
        if self.__animation == 'Attacking' or self.__animation == 'Hurt':
            if self.__FRAME_TO_WAIT > 0:
                return None

        return super().mover(*args)

    def atacar(self) -> bool:
        # Caso tenha morrido ou tomado dano, não vai atacar
        if self.__MORREU or self.__animation == 'Hurt':
            return False

        if self.__animation == 'Attacking':
            if self.__FRAME_TO_WAIT == 12:
                return True
            else:
                return False

        return False

    def update(self, hit_jogador: Hitbox) -> None:
        distancia = self._calcular_distancia(hit_jogador)

        # Update de qual a fonte de sprite, esquerda ou direita
        if self.direction == Direction.DIREITA_BAIXO or self.direction == Direction.DIREITA_CIMA or self.direction == Direction.DIREITA_MEIO:
            self.__animations = self.__animations_normal
        else:
            self.__animations = self.__animations_fliped

        # Update quanto a animação de atacar
        if self.__animation != 'Attacking' and self.__animation != 'Hurt':
            # Se não está atacando e não tomou hit
            if distancia < self.alcance - 3:  # Se está perto troca animação para atacar
                self.__set_animation('Attacking')

        # Update para cancelar ataque caso jogador saia do range ou caso tome hit
        if self.__animation == 'Attacking':
            if self._tomou_dano:
                if self.__will_damage_stop_attack():
                    self.__set_animation('Hurt')
            elif distancia > self.alcance + 10:
                self.__set_animation('Walking')

        return super().update(hit_jogador)

    @property
    def morreu(self) -> bool:
        if self.vida <= 0:
            if not self.__MORREU:
                self.__set_animation('Dying')
            else:
                if self.__ANIMACAO_RESETADA:
                    return True
                else:
                    return False
        return False

    def __get_current_animation(self) -> str:
        if self.__FRAME_TO_WAIT > 0:
            self.__FRAME_TO_WAIT -= 1
            return self.__animation

        if self._estado == Estado.REPOUSO:
            self.__set_animation('Repouso')
        elif self._estado == Estado.MORRENDO:
            self.__set_animation('Dying')
        elif self._estado == Estado.ALERTA:
            self.__set_animation('Procurando')
        elif self._tomou_dano:
            self.__set_animation('Hurt')
        elif self._estado == Estado.ATACANDO:
            self.__set_animation('Walking')

        return self.__animation

    def __set_animation(self, animation: str) -> None:
        # Animação não pode ser sobreposta
        if self.__animation == 'Dying':
            return None
        self.__FRAME_TO_WAIT = 0

        if animation == 'Attacking':
            self.__animation = animation
            self.__set_animation_frame_to_wait(animation)

        if animation == 'Dying':
            self.__MORREU = True
            self.__animation = animation
            self.__set_animation_frame_to_wait(animation)

        if animation == 'Hurt':
            self.__animation = animation
            self.__set_animation_frame_to_wait(animation)

        if animation == 'Walking':
            self.__animation = animation

        if animation == 'Repouso':
            if self.__ANIMACAO_RESETADA:
                self.__animation = self.__get_random_idle_animation()

        if animation == 'Procurando':
            if self.__ANIMACAO_RESETADA:
                self.__animation = self.__get_random_searching_animation()

    def __set_animation_frame_to_wait(self, animation: str) -> None:
        self.__FRAME_TO_WAIT = self.__animations_size[animation] // self.__animation_speed

    def __will_damage_stop_attack(self) -> bool:
        chance = random()

        if chance < self.__CHANCE_DAMAGE_STOP_ATTACK:
            return True
        else:
            return False

    def __get_random_idle_animation(self) -> str:
        if 0.1 > random():
            return 'Taunt'
        if 0.3 > random():
            return 'Idle Blink'
        else:
            return 'Idle'

    def __get_random_searching_animation(self) -> str:
        if 0.15 > random():
            return 'Taunt'
        else:
            return 'Walking'

    def __import_character_assets(self):
        character_path = 'Assets/Personagens/Minotauro/'
        self.__animations_size = {}
        self.__animations_normal = {}
        self.__animations_fliped = {}
        self.__animations = {
            'Idle': [], 'Walking': [], 'Taunt': [], 'Idle Blink': [],
            'Taunt': [], 'Attacking': [], 'Dying': [], 'Hurt': [],
        }

        for animation in self.__animations.keys():
            full_path = character_path + animation
            normal_images = import_folder(full_path, self.__tamanho_imagem)
            fliped_images = import_fliped_folder(full_path, self.__tamanho_imagem)
            self.__animations_fliped[animation] = fliped_images
            self.__animations_normal[animation] = normal_images
            self.__animations_size[animation] = len(normal_images)

            self.__animations = self.__animations_normal

    def _calibrar_dificuldade(self, dificuldade: Dificuldade) -> dict:
        if dificuldade.medio:
            return {
                'vida': 8, 'ataque': 2, 'defesa': 2,
                'vel': 2, 'vel_ataque': 1, 'arma_dano': 2,
                'arma_alcance': 10, 'view_distance': 150
            }
        elif dificuldade.dificil:
            return {
                'vida': 10, 'ataque': 6, 'defesa': 3,
                'vel': 2, 'vel_ataque': 1, 'arma_dano': 4,
                'arma_alcance': 10, 'view_distance': 150
            }
        else:  # Facil
            return {
                'vida': 6, 'ataque': 3, 'defesa': 1,
                'vel': 2, 'vel_ataque': 1, 'arma_dano': 1,
                'arma_alcance': 10, 'view_distance': 150
            }
