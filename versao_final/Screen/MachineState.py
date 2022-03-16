from Config.Enums import States
from Config.TelaJogo import TelaJogo
from Screen.States.AbstractState import AbstractState
from Screen.States.LoadGameState import LoadGameState
from Screen.States.MenuState import MenuState
from Screen.States.OptionsState import OptionsState
from typing import Dict, List
from Screen.States.PlayGameState import PlayGameState
from Screen.States.NewGameState import NewGameState
from Screen.States.PlayingState import PlayingState
from Screen.States.QuitState import QuitState
from pygame.event import Event


class StateMachine:
    def __init__(self) -> None:
        self.__states: Dict[States] = {
            States.MENU: MenuState(),
            States.OPTIONS: OptionsState(),
            States.QUIT: QuitState(),
            States.PLAY: PlayGameState(),
            States.NEW: NewGameState(),
            States.LOAD: LoadGameState(),
            States.PLAYING: PlayingState()}
        self.__current: AbstractState = self.__states[States.MENU]

    @property
    def current(self) -> AbstractState:
        return self.__current

    def run(self, events: List[Event]) -> None:
        next_state_enum = self.__current.run(events)
        self.__set_next_state(next_state_enum)

    def desenhar(self, tela: TelaJogo) -> None:
        self.__current.desenhar(tela)

    def stop(self) -> bool:
        if self.__current.state == States.QUIT:
            return True
        else:
            return False

    def __set_next_state(self, state: States) -> None:
        if state == States.SAME:
            return None

        next_state = self.__states[state]
        self.__current = next_state
