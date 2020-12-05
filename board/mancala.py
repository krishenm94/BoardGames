from board.board import Board, Result, PlayerTurn

import numpy as np

COLS = 7
INIT_SEEDS = 4


class Mancala(Board):
    """Player One's pits are pits 0 - 6 and Two's are 7 - 13
    Each last pit is the capture pit"""

    def __init__(self, cells=None, shape=(2, COLS)):
        super(Mancala, self).__init__(shape, cells)
        if cells is None:
            self.cells = np.array([INIT_SEEDS] * shape[0] * shape[1])
            self.cells[COLS - 1] = 0
            self.cells[2 * COLS - 1] = 0

    def execute_turn(self, move):
        assert self.cells[move] != 0, "Cell is empty"
        assert move != COLS - 1 and move != 2 * COLS - 1, "Cell is capture pit"

        seeds = self.cells[move]
        self.cells[move] = 0

        next_cell_index = move
        while seeds > 0:
            next_cell_index = (next_cell_index + 1) % (2 * COLS)
            if next_cell_index == COLS - 1 and self.whose_turn() == PlayerTurn.Two or \
                    next_cell_index == 2 * COLS - 1 and self.whose_turn() == PlayerTurn.One:
                continue

            self.cells[next_cell_index] += 1
            seeds -= 1

        self.moves_made += 1
        return

    def get_valid_moves(self, player_turn):
        assert 0 < player_turn < 3, "Invalid player turn."

        return [COLS * (player_turn - 1) + i for i in range(COLS - 1)
                if self.cells[i] > 0]

    def get_invalid_moves(self, player_turn):
        assert 0 < player_turn < 3, "Invalid player turn."

        return [COLS * (player_turn%2+1) + i for i in range(COLS - 1)
                if self.cells[i] == 0]

    def is_move_valid(self, move):
        if move > (self.cells.size - 1) or move < 0 or \
                self.cells[move] == 0 or \
                move == COLS - 1 and self.whose_turn() == PlayerTurn.Two or \
                move == 2 * COLS - 1 and self.whose_turn() == PlayerTurn.One:
            return False

        return True

    def get_game_result(self):
        seeds = self.get_uncaptured_seeds()

        assert seeds[PlayerTurn.One] != 0 or seeds[PlayerTurn.Two] != 0, \
            "Both players' non-capture pits are empty. Impossible position."

        if seeds[PlayerTurn.One] == 0:
            seeds[PlayerTurn.One] = self.cells[COLS - 1] + seeds[PlayerTurn.Two]
            seeds[PlayerTurn.Two] = self.cells[2 * COLS - 1]
        elif seeds[PlayerTurn.Two] == 0:
            seeds[PlayerTurn.Two] = self.cells[2 * COLS - 1] + seeds[PlayerTurn.One]
            seeds[PlayerTurn.One] = self.cells[COLS - 1]
        else:
            seeds[PlayerTurn.One] = self.cells[COLS - 1]
            seeds[PlayerTurn.Two] = self.cells[2 * COLS - 1]

        if seeds[PlayerTurn.One] > seeds[PlayerTurn.Two]:
            return seeds[PlayerTurn.One]
        elif seeds[PlayerTurn.Two] < seeds[PlayerTurn.One]:
            return seeds[PlayerTurn.Two]
        else:
            return 0  # Draw

    def get_uncaptured_seeds(self):
        seeds = {PlayerTurn.One: 0, PlayerTurn.Two: 0}

        for i in range(COLS - 1):
            seeds[PlayerTurn.One] += self.cells[i]
            seeds[PlayerTurn.Two] += self.cells[i + COLS]

        return seeds

    def is_game_over(self):
        seeds = self.get_uncaptured_seeds()

        assert seeds[PlayerTurn.One] != 0 or seeds[PlayerTurn.Two] != 0, \
            "Both players' non-capture pits are empty. Impossible position."

        return True if seeds[PlayerTurn.One] == 0 or seeds[PlayerTurn.Two] == 0 \
            else False

    def copy(self):
        new_board = Mancala(self.cells)
        new_board.moves_made = self.moves_made
        return new_board
