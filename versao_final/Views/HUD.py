from pygame import Rect, Surface, draw, font
from copy import deepcopy
from Config.Opcoes import Opcoes
from Config.TelaJogo import TelaJogo
from Personagens.Status import Status
from Utils.Folder import import_single_sprite


class HUD:
    __PATH = 'Assets/HUD/Fundo.png'
    __SIZE = Opcoes().TAMANHO_HUD
    __DEFENSE_POS = (530, 32)
    __STRENGTH_POS = (530, 70)
    __VEL_POS = (530, 110)
    __DAMAGE_POS = (655, 100)
    __SHIELD_POS = (773, 100)
    __CRITICAL_CHANCE_POS = (885, 100)
    __FONT = 'Agency FB'
    __LIFE_POS = (134, 48)
    __LIFE_SIZE = (297, 24)

    __ARROW_UP_PATH = 'Assets/HUD/ArrowUp.png'
    __ARROW_DOWN_PATH = 'Assets/HUD/ArrowDown.png'
    __ARROW_SIZE = (16, 15)

    __DEFENSE_ARROW_POS = (508, 23)
    __STRENGTH_ARROW_POS = (508, 60)
    __VEL_ARROW_POS = (506, 100)

    def __init__(self, status: Status) -> None:
        self.__status_inicial = deepcopy(status)
        self.__status = status
        self.__posicao = Opcoes().POSICAO_HUD
        self.__image = import_single_sprite(HUD.__PATH, HUD.__SIZE)
        self.__arrow_up = import_single_sprite(HUD.__ARROW_UP_PATH, HUD.__ARROW_SIZE)
        self.__arrow_down = import_single_sprite(HUD.__ARROW_DOWN_PATH, HUD.__ARROW_SIZE)
        self.__rect = self.__image.get_rect(topleft=self.__posicao)
        self.__text_size = 30
        self.__font = font.SysFont(HUD.__FONT, self.__text_size)
        self.__text_color = (149, 90, 29)

        self.__last_health = self.__status.vida
        self.__target_health = self.__status.vida
        self.__current_health = self.__status.vida
        self.__health_change_speed = 1
        self.__health_ratio = self.__status.vida_maxima / HUD.__LIFE_SIZE[0]

    def image(self) -> Surface:
        return self.__image

    def rect(self) -> Rect:
        return self.__rect

    def __update(self) -> None:
        damage_taken = False
        health_received = False
        health_diff = self.__status.vida - self.__last_health
        if health_diff < 0:
            damage_taken = True
        elif health_diff > 0:
            health_received = True

        if damage_taken:
            self.__target_health += health_diff
            if self.__target_health < 0:
                self.__target_health = 0
        if health_received:
            self.__target_health += health_diff
            if self.__target_health > self.__status.vida_maxima:
                self.__target_health = self.__status.vida_maxima

        self.__last_health = self.__status.vida

    def desenhar(self, tela: TelaJogo):
        self.__update()

        tela.janela.blit(self.__image, self.__rect)
        defesa = f'{self.__status.defesa}'
        vel = f'{self.__status.vel}'
        strength = f'{self.__status.ataque}'
        dano = f'3'
        defesa_escudo = f'3'
        chance_critica = f'3'

        defesa_surf = self.__font.render(defesa, False, self.__text_color)
        defesa_rect = defesa_surf.get_rect(center=HUD.__DEFENSE_POS)
        tela.janela.blit(defesa_surf, defesa_rect)

        vel_surf = self.__font.render(vel, False, self.__text_color)
        vel_rect = vel_surf.get_rect(center=HUD.__VEL_POS)
        tela.janela.blit(vel_surf, vel_rect)

        strength_surf = self.__font.render(strength, False, self.__text_color)
        strength_rect = strength_surf.get_rect(center=HUD.__STRENGTH_POS)
        tela.janela.blit(strength_surf, strength_rect)

        dano_surf = self.__font.render(dano, False, self.__text_color)
        dano_rect = dano_surf.get_rect(center=HUD.__DAMAGE_POS)
        tela.janela.blit(dano_surf, dano_rect)

        defesa_escudo_surf = self.__font.render(defesa_escudo, False, self.__text_color)
        defesa_escudo_rect = defesa_escudo_surf.get_rect(center=HUD.__SHIELD_POS)
        tela.janela.blit(defesa_escudo_surf, defesa_escudo_rect)

        chance_critica_surf = self.__font.render(chance_critica, False, self.__text_color)
        chance_critica_rect = chance_critica_surf.get_rect(center=HUD.__CRITICAL_CHANCE_POS)
        tela.janela.blit(chance_critica_surf, chance_critica_rect)

        self.__desenhar_vida(tela)
        self.__desenhar_efeitos(tela)

    def __desenhar_vida(self, tela: TelaJogo):
        health_bar_width = int(self.__current_health / self.__health_ratio)
        diff_health = self.__target_health - self.__current_health
        diff_width = int(diff_health / self.__health_ratio)

        # Perdendo vida
        if self.__current_health > self.__target_health:
            diff_color = (241, 105, 105)
            self.__current_health -= self.__health_change_speed
        # Ganhando Vida
        elif self.__current_health < self.__target_health:
            diff_color = (122, 0, 0)
            self.__current_health += self.__health_change_speed
        else:
            diff_color = (0, 0, 0)  # Vermelho

        health_rect = Rect(HUD.__LIFE_POS, (health_bar_width, HUD.__LIFE_SIZE[1]))
        diff_rect = Rect(health_rect.right, HUD.__LIFE_POS[1], diff_width, HUD.__LIFE_SIZE[1])
        diff_rect.normalize()

        draw.rect(tela.janela, (255, 0, 0), health_rect)
        draw.rect(tela.janela, diff_color, diff_rect)

    def __desenhar_efeitos(self, tela: TelaJogo):
        if self.__status.defesa > self.__status_inicial.defesa:
            rect = self.__arrow_up.get_rect(center=HUD.__DEFENSE_ARROW_POS)
            tela.janela.blit(self.__arrow_up, rect)
        elif self.__status.defesa > self.__status_inicial.defesa:
            rect = self.__arrow_down.get_rect(center=HUD.__DEFENSE_ARROW_POS)
            tela.janela.blit(self.__arrow_down, rect)

        if self.__status.ataque > self.__status_inicial.ataque:
            rect = self.__arrow_up.get_rect(center=HUD.__STRENGTH_ARROW_POS)
            tela.janela.blit(self.__arrow_up, rect)
        elif self.__status.ataque > self.__status_inicial.ataque:
            rect = self.__arrow_down.get_rect(center=HUD.__STRENGTH_ARROW_POS)
            tela.janela.blit(self.__arrow_down, rect)

        if self.__status.vel > self.__status_inicial.vel:
            rect = self.__arrow_up.get_rect(center=HUD.__VEL_ARROW_POS)
            tela.janela.blit(self.__arrow_up, rect)
        elif self.__status.vel > self.__status_inicial.vel:
            rect = self.__arrow_down.get_rect(center=HUD.__VEL_ARROW_POS)
            tela.janela.blit(self.__arrow_down, rect)
