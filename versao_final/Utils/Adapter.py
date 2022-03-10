from Config.Opcoes import Opcoes
from Config.Singleton import Singleton


class Adapter(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.__opcoes = Opcoes()

    def pygame_pos_to_matrix_index(self, position: tuple) -> tuple:
        position = self.__remove_offset_from_point(position)
        position = self.__inverter_ponto(position)
        position = self.__reduzir_ponto(position)

        return position

    def matrix_index_to_pygame_pos(self, position: tuple) -> tuple:
        position = self.__aumentar_ponto(position)
        position = self.__inverter_ponto(position)
        position = self.__apply_offset_to_point(position)

        return position

    def alcance_to_vector_dist(self, alcance: int) -> int:
        ratio = 100 / (self.__opcoes.MAX_ALCANCE - self.__opcoes.MIN_ALCANCE)
        aumento = alcance / ratio

        return self.__opcoes.MIN_ALCANCE + aumento

    def __inverter_ponto(self, position: tuple) -> tuple:
        return (position[1], position[0])

    def __remove_offset_from_point(self, ponto: tuple) -> tuple:
        return (ponto[0], ponto[1] - self.__opcoes.POSICAO_MAPAS[1])

    def __apply_offset_to_point(self, position: tuple) -> tuple:
        return (position[0], position[1] + self.__opcoes.POSICAO_MAPAS[1])

    def __reduzir_ponto(self, ponto: tuple) -> tuple:
        x = ponto[0] // self.__opcoes.MENOR_UNIDADE
        y = ponto[1] // self.__opcoes.MENOR_UNIDADE

        return (int(x), int(y))

    def __aumentar_ponto(self, ponto: tuple) -> tuple:
        x = ponto[0] * self.__opcoes.MENOR_UNIDADE
        y = ponto[1] * self.__opcoes.MENOR_UNIDADE

        return (x, y)
