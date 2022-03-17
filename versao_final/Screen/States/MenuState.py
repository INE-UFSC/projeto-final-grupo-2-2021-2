from Screen.States.AbstractState import AbstractState
from Screen.Views.MenuView import MenuView
from Config.Enums import States
from Sounds.MusicHandler import MusicHandler
from pygame.event import Event
from typing import List


class MenuState(AbstractState):
    __STATE = States.MENU
    __TELAS_MUSIC_PATH = 'Sounds/musics/som_menu.mp3'

    def __init__(self) -> None:
        view = MenuView()
        self.__music = MusicHandler()
        super().__init__(view, MenuState.__STATE)

    def run(self, events: List[Event]) -> States:
        self.__music.play_music(MenuState.__TELAS_MUSIC_PATH)
        return super().run(events)
