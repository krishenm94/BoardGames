from board.board import Board, Result
from board.board import PlayerTurn

from enum import IntEnum
import numpy as np


class Cell(IntEnum):
    Empty = 0
    O = -1  # player 2
    X = 1  # player 1


SIZE = 3


class TicTacToe(Board):
    """docstring for TicTacToe"""

    def __init__(self, cells=None, shape=(SIZE, SIZE)):
        super(TicTacToe, self).__init__(shape, cells)
        if cells is None:
            self.cells = np.array([Cell.Empty] * shape[0] * shape[1])

    def execute_turn(self, move):
        assert self.cells[move] == Cell.Empty, "Cell is not empty"

        self.cells[move] = self.get_cell_for_turn()
        return

    def get_cell_for_turn(self):
        if self.whose_turn() == PlayerTurn.One:
            return Cell.X
        else:
            return Cell.O

    def get_valid_moves(self):
        return [i for i in range(self.cells.size)
                if self.cells[i] == Cell.Empty]

    def get_invalid_moves(self):
        return [i for i in range(self.cells.size)
                if self.cells[i] != Cell.Empty]

    def cell_to_char(self, cell):

        if cell == Cell.Empty:
            return ' '

        if cell == Cell.X:
            return 'X'

        if cell == Cell.O:
            return 'O'

        assert False, "Undefined tic tac toe cell"

    def is_move_valid(self, move):
        if move > (self.shape[0] ** 2 - 1) or move < 0:
            return False

        if self.cells[move] == Cell.Empty:
            return True

        return False

    def get_game_result(self):
        rows_cols_and_diagonals = self.get_rows_cols_and_diagonals()

        sums = list(map(sum, rows_cols_and_diagonals))
        max_value = max(sums)
        min_value = min(sums)

        if max_value == self.shape[0]:
            return Result.One_Wins  # X player

        if min_value == -self.shape[0]:
            return Result.Two_Wins  # O player

        if not self.get_valid_moves():
            return Result.Draw

        return Result.Incomplete

    def get_rows_cols_and_diagonals(self):
        rows_and_diagonal = self.get_rows_and_diagonal(self.cells_2d())
        cols_and_antidiagonal = self.get_rows_and_diagonal(np.rot90(self.cells_2d()))
        return rows_and_diagonal + cols_and_antidiagonal

    def get_rows_and_diagonal(self, cells_2d):
        num_rows = cells_2d.shape[0]
        return ([row for row in cells_2d[range(num_rows), :]]
                + [cells_2d.diagonal()])

    def copy(self):
        return TicTacToe(self.cells)
