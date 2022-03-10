from Config.Opcoes import Opcoes
from Config.Enums import Direction, Estado
from Personagens.Inimigos.AbstractInimigo import AbstractInimigo
from Terrenos.AbstractTerreno import AbstractTerreno
from Utils.Folder import import_fliped_folder, import_folder
from Utils.Hitbox import Hitbox
from random import random
from pygame import Surface, Rect


class Minotauro(AbstractInimigo):
    __ANIMACOES_IMPORTADAS = False
    __CHANCE_DAMAGE_STOP_ATTACK = 0.5
    __TAMANHO_IMAGEM = (80, 65)
    __TAMANHO = (36, 48)
    __SPRITE_PATH = 'Assets/Personagens/Minotauro/'
    __STATS_FACIL = {'vida': 15, 'ataque': 4, 'defesa': 3, 'vel': 2, 'vel_ataque': 1, 'arma_dano': 3,
                     'arma_alcance': 18, 'view_distance': 150, 'transpassavel': False}
    __STATS_MEDIO = {'vida': 20, 'ataque': 5, 'defesa': 4, 'vel': 2, 'vel_ataque': 1, 'arma_dano': 4,
                     'arma_alcance': 18, 'view_distance': 150, 'transpassavel': False}
    __STATS_DIFICIL = {'vida': 25, 'ataque': 6, 'defesa': 5, 'vel': 3, 'vel_ataque': 1, 'arma_dano': 5,
                       'arma_alcance': 18, 'view_distance': 150, 'transpassavel': False}

    def __init__(self, terreno: AbstractTerreno, posicao=(0, 0)) -> None:
        stats = Minotauro.__calibrar_dificuldade()
        super().__init__(stats=stats, posicao=posicao, tamanho=Minotauro.__TAMANHO, terreno=terreno)

        if not Minotauro.__ANIMACOES_IMPORTADAS:
            Minotauro.__import_character_assets()
            Minotauro.__ANIMACOES_IMPORTADAS = True

        self.__animation = 'Idle'
        self.__frame_index = 0
        self.__animation_speed = 0.35
        self.__FRAME_TO_WAIT = 0
        self.__MORREU = False
        self.__LAST_ANIMATION = 'Idle'
        self.__ANIMACAO_RESETADA = False
        self.__DIST_PARA_ATAQUE = 8
        self.__animations = Minotauro.__normal_animations

    @classmethod
    def __import_character_assets(cls):
        cls.__animations_length = {}
        cls.__normal_animations = {}
        cls.__fliped_animations = {}

        animations_names = ['Idle', 'Walking', 'Taunt', 'Idle Blink',
                            'Taunt', 'Attacking', 'Dying', 'Hurt']

        for animation in animations_names:
            full_path = cls.__SPRITE_PATH + animation

            normal_images = import_folder(full_path, cls.__TAMANHO_IMAGEM)
            fliped_images = import_fliped_folder(full_path, cls.__TAMANHO_IMAGEM)

            cls.__fliped_animations[animation] = fliped_images
            cls.__normal_animations[animation] = normal_images
            cls.__animations_length[animation] = len(normal_images)

    @classmethod
    def __calibrar_dificuldade(cls) -> dict:
        dificuldade = Opcoes().dificuldade
        if dificuldade.medio:
            return cls.__STATS_MEDIO
        elif dificuldade.dificil:
            return cls.__STATS_DIFICIL
        else:
            return cls.__STATS_FACIL

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

    @rect.setter
    def rect(self, value: Rect) -> None:
        if type(value) == Rect:
            self.__rect = value

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
            self.__animations = Minotauro.__normal_animations
        else:
            self.__animations = Minotauro.__fliped_animations

        # Update quanto a animação de atacar
        if self.__animation != 'Attacking' and self.__animation != 'Hurt':
            # Se não está atacando e não tomou hit
            if distancia < self.__DIST_PARA_ATAQUE:  # Se está perto troca animação para atacar
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
                self.hitbox.transpassavel = True
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
        self.__FRAME_TO_WAIT = Minotauro.__animations_length[animation] // self.__animation_speed

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
