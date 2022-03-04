from abc import ABC, abstractmethod
from Enums.Enums import Dificuldade
from Personagens.Jogador.Jogador import Jogador
from Config.TelaJogo import TelaJogo
from Config.Opcoes import Opcoes
from Abstractions.AbstractTerreno import AbstractTerreno
from Enums.Enums import ComandosEnum
from Views.Telas.TelaPause import TelaPause


class AbstractFase(ABC):
    def __init__(self, jogador) -> None:
        self.__jogador = jogador
        self.__opcoes = Opcoes()
        self.__dificuldade = self.__opcoes.dificuldade
        self.__terreno = None

    def is_player_dead(self) -> bool:
        if self.__jogador.vida <= 0:
            return True
        else:
            return False

    def start(self, tela: TelaJogo):
        self.jogador.terreno = self.__terreno
        self.__terreno.iniciar_rodada(tela, self.jogador)

    def has_ended(self) -> bool:
        return self.__terreno.has_ended()

    def ciclo(self, tela: TelaJogo, pause) -> None:
        """Função para ser executada em todo ciclo do main loop"""
        if pause == False:
            self.__jogador.lidar_inputs()
            self.__terreno.mover_inimigos()
            self.__terreno.lidar_ataques(tela)
        else:
            self.tela_pause()
        self.__terreno.update()
        self.__terreno.desenhar(tela, self.__jogador)

    def tela_pause(self, *args, **kwargs) -> None:
        #telaPause = TelaPause()
        sim = True
        telaPause = TelaPause({
            ComandosEnum.TELA_JOGAR: self.__voltarJogo,
            ComandosEnum.LOAD_GAME: self.__salvar_jogo,
            ComandosEnum.TELA_OPCOES: self.__opcoes_pause,
            ComandosEnum.TELA_MENU: self.__voltarMenuPrincipal
        })
        telaPause.run()

    def __voltarJogo(self, *args, **kwargs):
        pass

    def __salvar_jogo(self, *args, **kwargs):
        pass

    def __opcoes_pause(self, *args, **kwargs):
        pass

    def __voltarMenuPrincipal(self, *args, **kwargs):
        pass

    @property
    def jogador(self) -> Jogador:
        return self.__jogador

    @property
    def terreno(self) -> AbstractTerreno:
        return self.__terreno

    @terreno.setter
    def terreno(self, value) -> None:
        if isinstance(value, AbstractTerreno):
            self.__terreno = value

    @property
    def dificuldade(self) -> Dificuldade:
        return self.__dificuldade

    @abstractmethod
    def load(self) -> None:
        pass
