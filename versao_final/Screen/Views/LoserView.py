from typing import List
from pygame import Rect, Surface, event
from Config.TelaJogo import TelaJogo
from Utils.Folder import import_single_sprite
from Config.Enums import States
from Screen.Views.AbstractView import AbstractView
from Screen.Components.Buttons import MenuButton, Button
from Screen.Components.Text import Text


class LoserView(AbstractView):
    __STATE = States.LOSER
    __IMAGE_PATH = 'Assets/Telas/3.1.jpg'
    __IMAGE_LOADED = False
    __IMAGE: Surface = None

    def __init__(self) -> None:
        super().__init__(LoserView.__STATE)

        if not LoserView.__IMAGE_LOADED:
            LoserView.__IMAGE = import_single_sprite(LoserView.__IMAGE_PATH, self._views_size)
            LoserView.__IMAGE_LOADED = True

        self.__image = LoserView.__IMAGE
        self.__rect = self.__image.get_rect(topleft=self._position)

        self.__texts: List[Text] = [
            Text((575, 240), 25, 'Loser ;-;')
        ]
        self.__buttons: List[Button] = [
            MenuButton('LEAVE', (575, 320), States.RESET),
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

    def run(self, events: List[event.Event]) -> States:
        for button in self.__buttons:
            button.run(events)

        leave_button = self.__buttons[0]
        if leave_button.clicked:
            return leave_button.next_state
        else:
            return States.SAME
