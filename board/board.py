from enum import IntEnum
import numpy as np


class PlayerTurn(IntEnum):
    One = 1,
    Two = 2


class Result(IntEnum):
    One_Wins = 1
    Two_Wins = -1
    Draw = 0
    Incomplete = 2


class Board(object):
    """docstring for Board"""

    def __init__(self, shape, cells=None):
        super(Board, self).__init__()

        self.shape = shape
        if cells is not None:
            self.cells = cells.copy()
        self.moves_made = 0

    def cells_2d(self):
        return self.cells.reshape(self.shape)

    def execute_turn(self, move):
        self.cells[move] = self.whose_turn()
        self.moves_made += 1
        return

    def whose_turn(self):
        return PlayerTurn.Two if self.moves_made % 2 == 1 else PlayerTurn.One

    def get_valid_moves(self, player_turn):
        return [i for i in range(self.cells.size)
                if self.cells[i] == 0]

    def get_invalid_moves(self, player_turn):
        return [i for i in range(self.cells.size)
                if self.cells[i] != 0]

    def simulate_turn(self, move):
        new_board = self.copy()
        new_board.execute_turn(move)
        return new_board

    def print(self):
        rows, cols = self.cells_2d().shape
        print('\n')

        for row in range(rows):
            print('|', end="")

            for col in range(cols):
                cell = self.cells_2d()[row][col]
                print(" %s " % self.cell_to_char(cell), end="|")

            if row < rows - 1:
                print("\n-", end="")
                for _ in range(cols):
                    print("----", end="")
                print("")

        print('\n')

    def cell_to_char(self, cell):
        return str(cell)

    def is_move_valid(self, move):
        if move > (self.shape[0] * self.shape[1] - 1) or move < 0:
            return False

        if self.cells[move] == 0:
            return True

        return False

    def is_game_over(self):
        return self.get_game_result() != Result.Incomplete

    def get_game_result(self):
        return Result.Incomplete

    def copy(self):
        new_board = Board(self.shape, self.cells)
        new_board.moves_made = self.moves_made
        return new_board
