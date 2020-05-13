import numpy as np


class Maze:
    def __init__(self, maze):
        self.WALL = 1
        self.FLOOR = 0
        self.PLAYER = 9
        self.FINISH = 7
        self.number_of_lines = len(open(maze).readlines())
        self.number_of_columns = 0
        self.Board = np.empty((0, self.number_of_lines), dtype=np.int16)

        with open(maze, "r") as reader:
            for line in reader:
                line = line.strip()
                line_list = []
                for char in line:
                    self.number_of_columns += 1
                    if char == "E":
                        char = 9
                    if char == "S":
                        char = 7
                    if char == "B":
                        char = 1
                    line_list.append(int(char))
                self.Board = np.append(self.Board, [line_list], axis=0)
            self.number_of_columns = int(self.number_of_columns / self.number_of_lines)

        self.ROWS = self.Board.shape[0]
        self.COLS = self.Board.shape[1]

        self.temp_start_position = np.where(self.Board == 9)
        self.temp_finish_position = np.where(self.Board == 7)
        self.fixed_start_position = (
            self.temp_start_position[0][0],
            self.temp_start_position[1][0],
        )
        self.fixed_finish_position = (
            self.temp_finish_position[0][0],
            self.temp_finish_position[1][0],
        )
        self.playerCurrentPosition = self.fixed_start_position
        self.finishPosition = self.fixed_finish_position

    def display(self):
        print(
            "Player Current Position: "
            + str(self.playerCurrentPosition[0])
            + ", "
            + str(self.playerCurrentPosition[1])
        )
        for line in self.Board:
            print(str(line) + "\n")

    def reset_player(self):
        if self.playerCurrentPosition != self.fixed_start_position:
            self.move_player_and_update_board(self.fixed_start_position)
        self.Board[self.fixed_finish_position[0]][
            self.fixed_finish_position[1]
        ] = self.FINISH

    def move_player_up(self):
        future_position = (
            self.playerCurrentPosition[0] - 1,
            self.playerCurrentPosition[1],
        )
        return self.move_player_and_update_board(future_position)

    def move_player_down(self):
        future_position = (
            self.playerCurrentPosition[0] + 1,
            self.playerCurrentPosition[1],
        )
        return self.move_player_and_update_board(future_position)

    def move_player_left(self):
        future_position = (
            self.playerCurrentPosition[0],
            self.playerCurrentPosition[1] - 1,
        )
        return self.move_player_and_update_board(future_position)

    def move_player_right(self):
        future_position = (
            self.playerCurrentPosition[0],
            self.playerCurrentPosition[1] + 1,
        )
        return self.move_player_and_update_board(future_position)

    def move_player_up_right(self):
        future_position = (
            self.playerCurrentPosition[0] - 1,
            self.playerCurrentPosition[1] + 1,
        )
        return self.move_player_and_update_board(future_position)

    def move_player_up_left(self):
        future_position = (
            self.playerCurrentPosition[0] - 1,
            self.playerCurrentPosition[1] - 1,
        )
        return self.move_player_and_update_board(future_position)

    def move_player_down_right(self):
        future_position = (
            self.playerCurrentPosition[0] + 1,
            self.playerCurrentPosition[1] + 1,
        )
        return self.move_player_and_update_board(future_position)

    def move_player_down_left(self):
        future_position = (
            self.playerCurrentPosition[0] + 1,
            self.playerCurrentPosition[1] - 1,
        )
        return self.move_player_and_update_board(future_position)

    def move_player_and_update_board(self, new_position):
        if self.is_wall(new_position):
            return self.WALL

        elif self.is_floor(new_position):
            self.Board[self.playerCurrentPosition[0]][
                self.playerCurrentPosition[1]
            ] = self.FLOOR
            self.Board[new_position[0]][new_position[1]] = self.PLAYER
            self.playerCurrentPosition = new_position
            return self.FLOOR

        elif self.is_finished(new_position):
            self.Board[self.playerCurrentPosition[0]][
                self.playerCurrentPosition[1]
            ] = self.FLOOR
            self.Board[new_position[0]][new_position[1]] = self.PLAYER
            self.playerCurrentPosition = new_position
            return self.FINISH

    def is_wall(self, move):
        if move[0] < 0 or move[1] < 0:
            return True
        if move[0] >= self.number_of_lines or move[1] >= self.number_of_columns:
            return True
        if self.Board[move[0]][move[1]] == self.WALL:
            return True

    def is_finished(self, move):
        return self.Board[move[0]][move[1]] == self.FINISH

    def is_floor(self, move):
        return self.Board[move[0]][move[1]] == self.FLOOR

    def decode_chromosome(self, chromosome):
        list_of_coordinates = []
        for i in chromosome:
            self.move_player(i)
            list_of_coordinates.append(self.playerCurrentPosition)
        return list_of_coordinates

    def move_player(self, move):
        if move == 0:
            return 0
        elif move == 1:
            return self.move_player_up()
        elif move == 2:
            return self.move_player_down()
        elif move == 3:
            return self.move_player_left()
        elif move == 4:
            return self.move_player_right()
        elif move == 5:
            return self.move_player_up_right()
        elif move == 6:
            return self.move_player_up_left()
        elif move == 7:
            return self.move_player_down_right()
        elif move == 8:
            return self.move_player_down_left()
