from typing import List
from pygame import Rect, Surface, event
from Config.TelaJogo import TelaJogo
from Screen.Components.Buttons import Button, MenuButton, MusicImageButton, SaveButton
from Utils.Folder import import_single_sprite
from Config.Enums import States
from Screen.Views.AbstractView import AbstractView


class PauseView(AbstractView):
    __STATE = States.PLAYING
    __IMAGE_PATH = 'Assets/Telas/FundoPause.jfif'
    __POS = (575, 375)
    __SIZE = (550, 450)
    __SIZE_SOM = (60, 60)
    __IMAGE_LOADED = False
    __IMAGE: Surface = None

    def __init__(self) -> None:
        rect = Rect(PauseView.__POS, PauseView.__SIZE)
        rect.center = rect.topleft
        position = rect.topleft

        super().__init__(PauseView.__STATE, position, PauseView.__SIZE)

        if not PauseView.__IMAGE_LOADED:
            PauseView.__IMAGE = import_single_sprite(PauseView.__IMAGE_PATH, self._views_size)
            PauseView.__IMAGE_LOADED = True

        self.__image = PauseView.__IMAGE
        self.__rect = self.__image.get_rect(topleft=self._position)

        self.__buttons: List[Button] = [
            MenuButton('CONTINUAR', (575, 320), States.SAME),
            SaveButton('SAVE', (575, 390), States.SAME),
            MenuButton('SAIR', (575, 460), States.MENU),
            MusicImageButton((760, 185), PauseView.__SIZE_SOM, (60, 60), States.SAME)
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
            button.desenhar(tela)

    def unpause(self) -> bool:
        continue_button = self.__buttons[0]
        if continue_button.clicked:
            return True
        else:
            return False

    def run(self, events: List[event.Event]) -> States:
        for button in self.__buttons:
            button.hover()
            button.run(events)

            next_state = button.get_state()
            if next_state != States.SAME:
                return next_state
        return States.SAME
