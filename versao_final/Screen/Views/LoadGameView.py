from DAO.JogoDAO import JogoDAO
from DAO.JogoOptions import JogoOptions
from Screen.Components.Text import Text
from typing import List
from pygame import Rect, Surface, event
from pygame import Rect, Surface
from Config.TelaJogo import TelaJogo
from Utils.Folder import import_single_sprite
from Config.Enums import States
from Screen.Components.Buttons import Button, MenuButton, SaveButton
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
        self.__active_save_button: SaveButton = None
        self.__jogoOptions = JogoOptions()
        self.__dao = JogoDAO()

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
            MenuButton('Start', self.__BTN_POS[5], States.LOAD_GAME),
            MenuButton('Delete', self.__BTN_POS[6], States.SAME),
            MenuButton('Return', self.__BTN_POS[7], States.PLAY)]
        self.__load_save_buttons()
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

    def __load_save_buttons(self) -> None:
        saves_names = self.__jogoOptions.get_all_names()
        if len(self.__buttons) > 3:
            self.__buttons = self.__buttons[:3]

        self.__buttons.extend([
            SaveButton(saves_names[0], self.__BTN_POS[0], States.SAME),
            SaveButton(saves_names[1], self.__BTN_POS[1], States.SAME),
            SaveButton(saves_names[2], self.__BTN_POS[2], States.SAME),
            SaveButton(saves_names[3], self.__BTN_POS[3], States.SAME),
            SaveButton(saves_names[4], self.__BTN_POS[4], States.SAME)])

    def run(self, events: List[event.Event]) -> States:
        for button in self.__buttons:
            button.hover()
            button.run(events)

        saves_buttons = self.__buttons[3:]
        for button in saves_buttons:
            if button.active:
                self.__active_save_button = button
                self.__jogoOptions.load_game_name = button.text

        start_button = self.__buttons[0]
        if start_button.clicked:
            if self.__active_save_button is None or self.__active_save_button.text == 'Empty':
                return States.SAME
            else:
                return start_button.next_state

        delete_button = self.__buttons[1]
        if delete_button.clicked:
            if self.__active_save_button is not None or self.__active_save_button.text == 'Empty':
                self.__dao.remove(self.__active_save_button.text)
                self.__load_save_buttons()

        return_button = self.__buttons[2]
        if return_button.clicked:
            return return_button.next_state
        return States.SAME
