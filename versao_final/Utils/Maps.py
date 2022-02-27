class MapUpdater():
    def __init__(self, matrix: list, invalid_char: str, valid_chars: list, invalid_not_updated_chars: list) -> None:
        self.__matrix = matrix
        self.__invalid_char = invalid_char
        self.__valid_chars = valid_chars
        self.__not_updated_invalid_chars = invalid_not_updated_chars

    def update_map_for_size(self, size) -> list:
        matrix = self.__matrix.copy()

        x_proporsion = size[0]
        y_proporsion = size[1]
        diagonal_proporsion = min(x_proporsion, y_proporsion)

        for x, linha in enumerate(matrix):
            for y, ponto in enumerate(linha):
                pontos_laterais = []
                pontos_laterais.extend(
                    self.__get_lateral_points_x_with_proporsion((x, y), x_proporsion))
                pontos_laterais.extend(
                    self.__get_lateral_points_y_with_proporsion((x, y), y_proporsion))
                pontos_laterais.extend(
                    self.__get_lateral_points_diagonal_with_proporsion((x, y), diagonal_proporsion))

                for ponto_lateral in pontos_laterais:
                    if self.__ponto_ocupado(ponto_lateral):
                        if ponto not in self.__not_updated_invalid_chars:
                            antes = matrix[x][0:y]
                            depois = matrix[x][y+1:]
                            matrix[x] = f'{antes}{self.__invalid_char}{depois}'
                            break

        return matrix

    def __ponto_ocupado(self, ponto: tuple):
        x = int(ponto[0])
        y = int(ponto[1])

        if x < 0 or x >= len(self.__matrix):
            return False

        if y < 0 or y >= len(self.__matrix[0]):
            return False

        if self.__matrix[x][y] in self.__valid_chars:
            return False

        return True

    def __get_lateral_points_x_with_proporsion(self, ponto: tuple, proporsion: int) -> list:
        pontos_laterais = []
        for x in range(1, proporsion):
            pontos_laterais.append((ponto[0] + x, ponto[1]))

        return pontos_laterais

    def __get_lateral_points_y_with_proporsion(self, ponto: tuple, proporsion: int) -> list:
        pontos_laterais = []
        for y in range(1, proporsion):
            pontos_laterais.append((ponto[0], ponto[1] + y))

        return pontos_laterais

    def __get_lateral_points_diagonal_with_proporsion(self, ponto: tuple, proporsion: int) -> list:
        pontos_laterais = []
        for x in range(1, proporsion):
            for y in range(1, proporsion):
                pontos_laterais.append((ponto[0] + x, ponto[1] + y))

        return pontos_laterais
