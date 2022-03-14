from pygame import mixer
from Config.Singleton import Singleton
from Config.Opcoes import Opcoes


class MusicHandler(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.__opcoes = Opcoes()
            self.__PLAYING_MUSIC = False
            mixer.init()

    def play_music(self, music_path: str) -> None:
        if music_path == '':
            return

        try:
            if self.__PLAYING_MUSIC:
                mixer.music.stop()

            mixer.music.load(music_path)
            mixer.music.play(-1)
            self.__PLAYING_MUSIC = True
        except Exception as e:
            print(f'Error Playing Music: {e}')

    def play_sound(self, sound_path: str) -> None:
        if sound_path == '':
            return
        try:
            sound = mixer.Sound(sound_path)
            sound.play()
        except Exception as e:
            print(f'Error Playing Music: {e}')
        pass

    def update(self) -> None:
        if not self.__opcoes.tocar_musica:
            if self.__PLAYING_MUSIC:
                mixer.music.set_volume(0)
                self.__PLAYING_MUSIC = False
        else:
            if not self.__PLAYING_MUSIC:
                mixer.music.set_volume(60)
                self.__PLAYING_MUSIC = True
