from random import choice


class AbstractMap:
    def __init__(self, matrix: list) -> None:
        self.__input_matrix = matrix.copy()
        self.__obstacles_char = ['P', '0', '1', '2']
        self.__block_position_and_vision_char = 'P'
        self.__block_only_movement_char = '0'
        self.__block_only_vision_char = '1'
        self.__non_block_char = '2'

        self.__start_player_position = self.__get_start_player_position()
        self.__enemies_start_position = self.__get_all_enemies_position()
        self.__matrix = self.__get_matrix_with_only_obstacles(matrix)

        self.__set_all_positions_blocking()

    def get_matrix_only_obstacles(self) -> list:
        return self.__matrix.copy()

    @property
    def player_start_position(self) -> tuple:
        return self.__start_player_position

    def get_random_enemy_position(self) -> tuple:
        return choice(self.__enemies_start_position)

    @property
    def positions_blocking_movement_and_vision(self) -> list:
        return self.__positions_blocking_vision_and_movement

    @property
    def positions_blocking_only_movement(self) -> list:
        return self.__positions_blocking_only_movement

    @property
    def positions_blocking_only_vision(self) -> list:
        return self.__positions_blocking_only_vision

    @property
    def positions_blocking_nothing(self) -> list:
        return self.__positions_blocking_nothing

    @property
    def positions_blocking_movement(self) -> list:
        return self.__position_blocking_movement

    @property
    def positions_blocking_vision(self) -> list:
        return self.__position_blocking_vision

    def is_position_valid(self, posicao: tuple) -> bool:
        x = int(posicao[0])
        y = int(posicao[1])

        if x < 0 or x >= len(self.__matrix):
            print(f'Acesso indevido a matriz em [{x}][{y}] - 3')
            return False

        if y < 0 or y >= len(self.__matrix[0]):
            print(f'Acesso indevido a matriz em [{x}][{y}] - 4')
            return False

        return True

    def __set_all_positions_blocking(self) -> None:
        positions_blocking_both = []
        positions_blocking_vision = []
        positions_blocking_movement = []
        positions_blocking_nothing = []

        for pos_y, linha in enumerate(self.__input_matrix):
            for pos_x, cell in enumerate(linha):
                position = (pos_y, pos_x)

                if cell == self.__block_position_and_vision_char:
                    positions_blocking_both.append(position)
                elif cell == self.__block_only_movement_char:
                    positions_blocking_movement.append(position)
                elif cell == self.__block_only_vision_char:
                    positions_blocking_vision.append(position)
                elif cell == self.__non_block_char:
                    positions_blocking_nothing.append(position)

        self.__positions_blocking_vision_and_movement = positions_blocking_both
        self.__positions_blocking_only_movement = positions_blocking_movement
        self.__positions_blocking_only_vision = positions_blocking_vision
        self.__positions_blocking_nothing = positions_blocking_nothing

        self.__position_blocking_movement = positions_blocking_movement
        self.__position_blocking_movement.extend(positions_blocking_both)

        self.__position_blocking_vision = positions_blocking_vision
        self.__position_blocking_vision.extend(positions_blocking_both)

    def __get_matrix_with_only_obstacles(self, matrix_input: list) -> list:
        matrix = matrix_input.copy()

        for pos_x, linha in enumerate(matrix):
            for pos_y, cell in enumerate(linha):
                if cell not in self.__obstacles_char and cell != ' ':
                    linha = self.__trocar_char_in_string(linha, pos_y, ' ')
            matrix[pos_x] = linha

        return matrix

    def __get_all_enemies_position(self) -> list:
        enemies_positions = []

        for pos_x, linha in enumerate(self.__input_matrix):
            for pos_y, cell in enumerate(linha):
                if cell == '5':
                    position = (pos_x, pos_y)
                    enemies_positions.append(position)

        return enemies_positions

    def __get_start_player_position(self) -> list:
        for pos_x, linha in enumerate(self.__input_matrix):
            for pos_y, cell in enumerate(linha):
                if cell == 'J':
                    position = (pos_x, pos_y)
                    return position

    def __trocar_char_in_string(self, string_input: str, pos: int, new_char: str) -> str:
        antes = string_input[0:pos]
        depois = string_input[pos+1:]
        return f'{antes}{new_char}{depois}'


matrix_dungeon = [
    #          X         X         X         X
    # 01234567890123456789012345678901234567890123456
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',  # 0
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',  # 1
    'PP00      00PP00                PP0          PP',  # 2
    'PP        00PP00                PP  5        PP',  # 3
    'PP    5     PP     5   5   5    PP           PP',  # 4
    'PP          PP                  PP       5   PP',  # 5
    'PP   5      PP                  PP           PP',  # 6
    'PP         0PP                  PP           PP',  # 7
    'PP5   PPPPPPPP                  PP   PPPPPPPPPP',  # 8
    'PP    PPPPPPPP                  PP   PPPPPPPPPP',  # 9c
    'PP         0PP      5                        PP',  # 10
    'PP    5     PP                            5  PP',  # 11
    'PP          PP      PPPPPPPP 5               PP',  # 12
    'PP          PP      PPPPPPPP              5  PP',  # 13
    'PP 5        PP      PPPPPPPP                 PP',  # 14
    'PP        00PP      PPPPPPPP 5       PPPPPPPPPP',  # 15
    'PP    PPPPPPPP      PPPPPPPP         PPPPPPPPPP',  # 16
    'PP    PPPPPPPP      PPPPPPPP         PPPPPPPPPP',  # 17
    'PP                     PP            PPPPPPPPPP',  # 18
    'PP     5       5       PP            P       PP',  # 19
    'PP                     PP            P       PP',  # 20
    'PP             000     PP                 J  PP',  # 21
    'PP    5        000     PP                  00PP',  # 22
    'PP             000     PP                  00PP',  # 23
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',  # 24
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP']  # 25

# A parede no canto inferior direito fica nos quadrados 46x25
