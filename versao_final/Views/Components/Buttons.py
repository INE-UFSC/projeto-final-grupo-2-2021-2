from abc import ABC, abstractmethod
from typing import Any
from Config.Opcoes import Opcoes
from Config.Enums import Dificuldade, States
from Sounds.MusicHandler import MusicHandler
from Config.TelaJogo import TelaJogo
from Utils.Folder import import_single_sprite
from pygame import Rect, draw, font, MOUSEBUTTONUP
import pygame


class Button(ABC):
    def __init__(self, position, size, next_state: States) -> None:
        self.__position = position
        self.__size = size
        self.__next_state = next_state

        self.__hover_color = (255, 50, 50)
        self.__normal_color = (200, 125, 125)

        self.__rect = Rect(self.__position, self.__size)
        self.__color = self.__normal_color

    def _button_clicked(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    return True
        return False

    def hover(self) -> None:
        if self.__rect.collidepoint(pygame.mouse.get_pos()):
            self.__color = self.__hover_color
        else:
            self.__color = self.__normal_color

    @property
    def rect(self) -> Rect:
        return self.__rect

    @property
    def next_state(self) -> Any:
        return self.__next_state

    @abstractmethod
    def desenhar(self, tela: TelaJogo) -> None:
        draw.rect(tela.janela, self.__color, self.__rect, 3, 8)

    @abstractmethod
    def get_state(self) -> States:
        pass


class TextButton(Button):
    def __init__(self, text, position, size, next_state: States) -> None:
        rect = Rect(position, size)
        rect.center = rect.topleft
        position = rect.topleft

        super().__init__(position, size, next_state)
        self.__color = (255, 255, 255)
        self.__text = text
        self.__font = font.SysFont('Agency FB', 25)
        self.__text = self.__font.render(text, True, self.__color)
        self.__text_rect = self.__text.get_rect(center=rect.center)

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, value) -> None:
        if type(value) == str:
            self.__text = self.__font.render(value, True, self.__color)

    def desenhar(self, tela: TelaJogo) -> None:
        super().desenhar(tela)
        tela.janela.blit(self.__text, self.__text_rect)

    def get_state(self) -> States:
        if super()._button_clicked():
            return self.next_state
        else:
            return States.SAME


class ImageButton(Button):
    def __init__(self, position, size, path, scale, next_state: States) -> None:
        super().__init__(position, size, next_state)
        self.__image = import_single_sprite(path, scale)
        self.__rect = self.__image.get_rect(center=position)

    def desenhar(self, tela: TelaJogo) -> None:
        super().desenhar(tela)
        tela.janela.blit(self.__image, self.__rect)

    def get_state(self) -> States:
        if super()._button_clicked():
            return self.next_state
        else:
            return States.SAME


class MenuButton(TextButton):
    __SIZE = (130, 45)

    def __init__(self, text, position, next_state: States) -> None:
        super().__init__(text, position, MenuButton.__SIZE, next_state)


class ImageTextButton(ImageButton):
    def __init__(self, position, size, path, scale, next_state: States) -> None:
        path = 'Assets/Telas/botao.png'
        scale = (100, 35)
        super().__init__(position, size, path, scale, next_state)
        TextButton.__init__(self, 'Test', position, size, next_state)

    def desenhar(self, tela: TelaJogo) -> None:
        ImageButton.desenhar(tela)
        TextButton()


class MusicButton(TextButton):
    __SIZE = (130, 45)

    def __init__(self, position, next_state: States) -> None:
        self.__music = MusicHandler()
        text = self.__get_current_music_status_text()
        super().__init__(text, position, MusicButton.__SIZE, next_state)

    def get_state(self) -> States:
        if super()._button_clicked():
            self.__executar()
            return self.next_state
        else:
            return States.SAME

    def __get_current_music_status_text(self) -> str:
        if self.__music.playing:
            return 'Music: On'
        else:
            return 'Music: Off'

    def __executar(self) -> None:
        self.__music.toggle_pause()

    def __update(self) -> None:
        self.text = self.__get_current_music_status_text()

    def desenhar(self, tela: TelaJogo) -> None:
        self.__update()
        super().desenhar(tela)


class ButtonDificil(MenuButton):
    def __init__(self, text, position, next_state: States) -> None:
        super().__init__(text, position, next_state)

    def get_state(self) -> States:
        if super()._button_clicked():
            self.__executar()
            return self.next_state
        else:
            return States.SAME

    def __executar(self) -> None:
        self.__opcoes = Opcoes()
        self.__opcoes.dificuldade = Dificuldade.dificil


class ButtonMedio(MenuButton):
    def __init__(self, text, position, next_state: States) -> None:
        super().__init__(text, position, next_state)

    def get_state(self) -> States:
        if super()._button_clicked():
            self.__executar()
            return self.next_state
        else:
            return States.SAME

    def __executar(self) -> None:
        self.__opcoes = Opcoes()
        self.__opcoes.dificuldade = Dificuldade.medio


class ButtonFacil(MenuButton):
    def __init__(self, text, position, next_state: States) -> None:
        super().__init__(text, position, next_state)

    def get_state(self) -> States:
        if super()._button_clicked():
            self.__executar()
            return self.next_state
        else:
            return States.SAME

    def __executar(self) -> None:
        self.__opcoes = Opcoes()
        self.__opcoes.dificuldade = Dificuldade.facil
