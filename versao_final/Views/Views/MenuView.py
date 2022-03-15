from Views.Components.Text import Text
from typing import List
from pygame import Rect, Surface
from Config.TelaJogo import TelaJogo
from Utils.Folder import import_single_sprite
from Config.Enums import States
from Views.Components.Buttons import Button, MenuButton
from Views.Views.AbstractView import AbstractView


class MenuView(AbstractView):
    __STATE = States.MENU
    __IMAGE_PATH = 'Assets/Telas/3.1.jpg'
    __IMAGE_LOADED = False
    __IMAGE: Surface = None

    def __init__(self) -> None:
        super().__init__(MenuView.__STATE)

        if not MenuView.__IMAGE_LOADED:
            MenuView.__IMAGE = import_single_sprite(MenuView.__IMAGE_PATH, self._views_size)
            MenuView.__IMAGE_LOADED = True

        self.__image = MenuView.__IMAGE
        self.__rect = self.__image.get_rect(topleft=self._position)

        self.__BTN_POS = [
            (self._views_size[0]/2, self._views_size[0]/2 - 250),
            (self._views_size[0]/2, self._views_size[0]/2 - 175),
            (self._views_size[0]/2, self._views_size[0]/2 - 100)]
        self.__buttons: List[Button] = [
            MenuButton('PLAY', self.__BTN_POS[0], States.PLAY),
            MenuButton('OPTIONS', self.__BTN_POS[1], States.OPTIONS),
            MenuButton('QUIT', self.__BTN_POS[2], States.QUIT)]

        self.__TEXT_POS = [
            (self._views_size[0]/2, 100)]
        self.__texts: List[Text] = [
            Text(self.__TEXT_POS[0], 60, 'The Binding Of Isaac')
        ]

    @property
    def image(self) -> Surface:
        return self.__image

    @property
    def rect(self) -> Rect:
        return self.__rect

    def desenhar(self, tela: TelaJogo) -> None:
        super().desenhar(tela)
        for button in self.__buttons:
            button.hover()
            button.desenhar(tela)
        for text in self.__texts:
            text.desenhar(tela)

    def run(self) -> States:
        for button in self.__buttons:
            state = button.get_state()

            if state != States.SAME:
                return state
        return States.SAME
