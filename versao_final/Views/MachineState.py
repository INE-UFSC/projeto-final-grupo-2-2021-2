from Config.Enums import States
from Config.TelaJogo import TelaJogo
from Views.States.AbstractState import AbstractState
from Views.States.MenuState import MenuState
from Views.States.OptionsState import OptionsState
from typing import Dict


class StateMachine:
    def __init__(self) -> None:
        self.__states: Dict[States] = {
            States.MENU: MenuState(),
            States.OPTIONS: OptionsState()}
        self.__current: AbstractState = self.__states[States.MENU]

    @property
    def current(self) -> AbstractState:
        return self.__current

    def run(self) -> None:
        next_state_enum = self.__current.run()
        self.__set_next_state(next_state_enum)

    def desenhar(self, tela: TelaJogo) -> None:
        self.__current.desenhar(tela)

    def __set_next_state(self, state: States) -> None:
        if state == States.SAME:
            return None

        print(state)
        next_state = self.__states[state]
        self.__current = next_state
