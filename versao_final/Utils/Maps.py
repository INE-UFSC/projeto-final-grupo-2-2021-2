def update_invalid_position_in_map_for_size(matrix_input: list, size: tuple, invalid_char: str, ignored_chars: list) -> list:
    matrix = matrix_input.copy()

    x_proporsion = size[0]
    y_proporsion = size[1]

    matrix_x = __update_map_for_proporsion_x(matrix, x_proporsion, invalid_char, ignored_chars)
    matrix_y = __update_map_for_proporsion_y(matrix, y_proporsion, invalid_char, ignored_chars)

    merged_map = __merge_maps(matrix_x, matrix_y, invalid_char)

    return merged_map


def __update_map_for_proporsion_x(matrix_input: list, x_proporsion: int, invalid_char: str, ignored_chars: list) -> list:
    matrix = matrix_input.copy()

    def determinar_ponto_atingivel(ponto):
        pontos_laterais = []
        for x in range(1, x_proporsion):
            pontos_laterais.append((ponto[0] + x, ponto[1]))

        for ponto_lateral in pontos_laterais:
            if not __ponto_dentro_da_matriz_e_nao_ignorado(matrix, ponto_lateral, ignored_chars):
                if matrix[ponto[0]][ponto[1]] != 'P':
                    antes = matrix[ponto[0]][0:ponto[1]]
                    depois = matrix[ponto[0]][ponto[1]+1:]
                    matrix[ponto[0]] = f'{antes}{invalid_char}{depois}'

    for index_row, linha in enumerate(matrix):
        for index_column, cell in enumerate(linha):
            determinar_ponto_atingivel((index_row, index_column))

    return matrix


def __update_map_for_proporsion_y(matrix_input: list, y_proporsion: int, invalid_char: str, ignored_chars: list) -> list:
    matrix = matrix_input.copy()

    def determinar_ponto_atingivel(ponto):
        pontos_laterais = []
        for x in range(1, y_proporsion):
            pontos_laterais.append((ponto[0], ponto[1] + x))

        for ponto_lateral in pontos_laterais:
            if not __ponto_dentro_da_matriz_e_nao_ignorado(matrix, ponto_lateral, ignored_chars):
                if matrix[ponto[0]][ponto[1]] != 'P':
                    antes = matrix[ponto[0]][0:ponto[1]]
                    depois = matrix[ponto[0]][ponto[1]+1:]
                    matrix[ponto[0]] = f'{antes}{invalid_char}{depois}'

    for index_row, linha in enumerate(matrix):
        for index_column, cell in enumerate(linha):
            determinar_ponto_atingivel((index_row, index_column))

    return matrix


def __merge_maps(matrix1: list, matrix2: list, invalid_char: str) -> list:
    for index_x, linha in enumerate(matrix1):
        for index_y, cell in enumerate(linha):
            if cell == invalid_char:
                antes = matrix2[index_x][0:index_y]
                depois = matrix2[index_x][index_y+1:]

                matrix2[index_x] = f'{antes}{invalid_char}{depois}'

    return matrix2


def __ponto_dentro_da_matriz_e_nao_ignorado(matrix: list, ponto: tuple, ignored_chars: list) -> bool:
    x = int(ponto[0])
    y = int(ponto[1])

    if x < 0 or x >= len(matrix):
        return False

    if y < 0 or y >= len(matrix[0]):
        return False

    if matrix[x][y] in ignored_chars:
        return False

    return True
