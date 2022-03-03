from cgitb import text
from msilib.schema import Font
from pygame import Rect, Surface
from copy import deepcopy

import pygame
from Config.Opcoes import Opcoes
from Config.TelaJogo import TelaJogo
from Personagens.Status import Status
from Utils.Folder import import_single_sprite


class HUD:
    __PATH = 'Assets/HUD/Fundo.png'
    __SIZE = Opcoes().TAMANHO_HUD
    __DEFENSE_POS = (525, 34)
    __STRENGTH_POS = (525, 70)
    __VEL_POS = (525, 110)
    __DAMAGE_POS = (650, 110)
    __SHIELD_POS = (775, 110)
    __CRITICAL_CHANCE_POS = (885, 110)

    def __init__(self, status: Status) -> None:
        self.__status_inicial = deepcopy(status)
        self.__status = status
        self.__posicao = Opcoes().POSICAO_HUD
        self.__image = import_single_sprite(HUD.__PATH, HUD.__SIZE)
        self.__rect = self.__image.get_rect(topleft=self.__posicao)
        self.__text_size = 20
        self.__font = self.__load_font()
        self.__color = (149, 90, 29)

    def __load_life_bars(self) -> Surface:
        pass

    def __load_font(self) -> Font:
        return pygame.font.SysFont('Candara', self.__text_size)

    def image(self) -> Surface:
        return self.__image

    def rect(self) -> Rect:
        return self.__rect

    def update(self) -> None:
        pass

    def desenhar(self, tela: TelaJogo):
        tela.janela.blit(self.__image, self.__rect)
        defesa = f'{self.__status.defesa}'
        vel = f'{self.__status.vel}'
        strength = f'{self.__status.ataque}'
        dano = f'X'
        defesa_escudo = f'X'
        chance_critica = f'X'

        defesa_surf = self.__font.render(defesa, False, self.__color)
        defesa_rect = defesa_surf.get_rect(center=HUD.__DEFENSE_POS)
        tela.janela.blit(defesa_surf, defesa_rect)

        vel_surf = self.__font.render(vel, False, self.__color)
        vel_rect = vel_surf.get_rect(center=HUD.__VEL_POS)
        tela.janela.blit(vel_surf, vel_rect)

        strength_surf = self.__font.render(strength, False, self.__color)
        strength_rect = strength_surf.get_rect(center=HUD.__STRENGTH_POS)
        tela.janela.blit(strength_surf, strength_rect)

        dano_surf = self.__font.render(dano, False, self.__color)
        dano_rect = dano_surf.get_rect(center=HUD.__DAMAGE_POS)
        tela.janela.blit(dano_surf, dano_rect)

        defesa_escudo_surf = self.__font.render(defesa_escudo, False, self.__color)
        defesa_escudo_rect = defesa_escudo_surf.get_rect(center=HUD.__SHIELD_POS)
        tela.janela.blit(defesa_escudo_surf, defesa_escudo_rect)

        chance_critica_surf = self.__font.render(chance_critica, False, self.__color)
        chance_critica_rect = chance_critica_surf.get_rect(center=HUD.__CRITICAL_CHANCE_POS)
        tela.janela.blit(chance_critica_surf, chance_critica_rect)
