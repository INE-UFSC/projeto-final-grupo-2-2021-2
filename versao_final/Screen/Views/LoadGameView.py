from Screen.Components.Text import Text
from typing import List
from pygame import Rect, Surface, event
from pygame import Rect, Surface
from Config.TelaJogo import TelaJogo
from Utils.Folder import import_single_sprite
from Config.Enums import States
from Screen.Components.Buttons import Button, MenuButton
from Screen.Views.AbstractView import AbstractView


class LoadGameView(AbstractView):
    __STATE = States.LOAD
    __IMAGE_PATH = 'Assets/Telas/3.1.jpg'
    __IMAGE_LOADED = False
    __IMAGE: Surface = None

    def __init__(self) -> None:
        super().__init__(LoadGameView.__STATE)

        if not LoadGameView.__IMAGE_LOADED:
            LoadGameView.__IMAGE = import_single_sprite(LoadGameView.__IMAGE_PATH, self._views_size)
            LoadGameView.__IMAGE_LOADED = True

        self.__image = LoadGameView.__IMAGE
        self.__rect = self.__image.get_rect(topleft=self._position)

        self.__BTN_POS = [
            (self._views_size[0]*2/10, self._views_size[1]/2 - 100),
            (self._views_size[0]*2/10, self._views_size[1]/2 - 25),
            (self._views_size[0]*2/10, self._views_size[1]/2 + 50),
            (self._views_size[0]*2/10, self._views_size[1]/2 + 125),
            (self._views_size[0]*2/10, self._views_size[1]/2 + 200),
            (self._views_size[0]*8/10, self._views_size[1]/2 - 50),
            (self._views_size[0]*8/10, self._views_size[1]/2 + 25),
            (self._views_size[0]*8/10, self._views_size[1]/2 + 100)
        ]

        self.__buttons: List[Button] = [
            MenuButton('Save1', self.__BTN_POS[0], States.SAME),
            MenuButton('Save2', self.__BTN_POS[1], States.SAME),
            MenuButton('Save3', self.__BTN_POS[2], States.SAME),
            MenuButton('Save4', self.__BTN_POS[3], States.SAME),
            MenuButton('Save5', self.__BTN_POS[4], States.SAME),
            MenuButton('Start', self.__BTN_POS[5], States.PLAYING),
            MenuButton('Delete', self.__BTN_POS[6], States.SAME),
            MenuButton('Return', self.__BTN_POS[7], States.PLAY)]
        self.__TEXT_POS = [
            (self._views_size[0]/2, 100),
            (self._views_size[0]*2/10, self._views_size[1]/2 - 150)
        ]
        self.__texts: List[Text] = [
            Text(self.__TEXT_POS[0], 60, 'Load Game'),
            Text(self.__TEXT_POS[1], 25, 'Available Saves:')
        ]

    @ property
    def image(self) -> Surface:
        return self.__image

    @ property
    def rect(self) -> Rect:
        return self.__rect

    def desenhar(self, tela: TelaJogo) -> None:
        super().desenhar(tela)
        for button in self.__buttons:
            button.desenhar(tela)
        for text in self.__texts:
            text.desenhar(tela)

    def run(self, events: List[event.Event]) -> States:
        for button in self.__buttons:
            button.hover()
            button.run(events)
            state = button.get_state()

            if state != States.SAME:
                return state
        return States.SAME
