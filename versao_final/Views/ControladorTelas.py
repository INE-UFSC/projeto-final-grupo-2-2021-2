from pickle import FALSE
from Config.TelaJogo import TelaJogo
from Sounds.MusicHandler import MusicHandler
from Views.MachineState import StateMachine
import pygame


class ControladorTelas:
    __TELAS_MUSIC_PATH = 'Sounds/musics/som_menu.mp3'

    def __init__(self) -> None:
        pygame.init()
        self.__tela = TelaJogo()
        self.__music = MusicHandler()
        self.__machine = StateMachine()
        self.__FPS = 40

    def start(self) -> None:
        self.__tela.mostrar_fundo()
        self.__music.play_music(ControladorTelas.__TELAS_MUSIC_PATH)
        self._run()

    def _run(self) -> None:
        clock = pygame.time.Clock()

        MAIN_LOOP = True
        while MAIN_LOOP:
            clock.tick(self.__FPS)
            self.__machine.desenhar(self.__tela)
            self.__machine.run()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    MAIN_LOOP = False
                    pygame.quit()
                    exit()

            pygame.display.update()