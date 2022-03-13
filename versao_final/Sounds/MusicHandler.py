from pygame import mixer
from Config.Singleton import Singleton


class MusicHandler(Singleton):
    def __init__(self) -> None:
        if not super().created:
            mixer.init()
            self.__PLAYING_MUSIC = False

    def play_music(self, music_path: str) -> None:
        try:
            if self.__PLAYING_MUSIC:
                mixer.music.stop()

            mixer.music.load(music_path)
            mixer.music.play()
            self.__PLAYING_MUSIC = True
        except Exception as e:
            print(f'Error Playing Music: {e}')

    def play_sound(self, sound_path: str) -> None:
        try:
            sound = mixer.Sound(sound_path)
            sound.play()
        except Exception as e:
            print(f'Error Playing Music: {e}')
        pass
