from board.board import Board

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
        assert self.cells[move] != 0, f"Cell is empty, Invalid move: {move}"
        assert move != COLS - 1 and move != 2 * COLS - 1, "Cell is capture pit"

        seeds = self.cells[move]
        self.cells[move] = 0

        next_index = move
        while seeds > 0:
            next_index = (next_index + 1) % (2 * COLS)

            # Skip pit if it's the opponent's capture pit
            if next_index == COLS - 1 and self.whose_turn() == 2 or \
                    next_index == 2 * COLS - 1 and self.whose_turn() == 1:
                continue

            self.cells[next_index] += 1
            seeds -= 1

        # Capture opposite pit if last seed ends in an empty pit on player's side
        if self.cells[next_index] == 1:

            if self.whose_turn() == 1 and -1 < next_index < COLS - 1:

                opposite_index = 2 * COLS - 2 - next_index
                self.cells[COLS - 1] += self.cells[next_index] + self.cells[opposite_index]
                self.cells[next_index] = 0
                self.cells[opposite_index] = 0

            elif self.whose_turn() == 2 and COLS - 1 < next_index < 2 * COLS - 1:

                opposite_index = COLS * 2 - 2 - next_index
                self.cells[2 * COLS - 1] += self.cells[next_index] + self.cells[opposite_index]
                self.cells[next_index] = 0
                self.cells[opposite_index] = 0

        # Get extra turn if last pit was capture pit
        if next_index == COLS - 1 and self.whose_turn() == 1 or \
                next_index == 2 * COLS - 1 and self.whose_turn() == 2:
            return

        self.moves_made += 1
        return

    def get_valid_moves(self, player_turn):
        assert 0 < player_turn < 3, "Invalid player turn."

        return [COLS * (player_turn - 1) + i for i in range(COLS - 1)
                if self.cells[COLS * (player_turn - 1) + i] > 0]

    def get_invalid_moves(self, player_turn):
        assert 0 < player_turn < 3, "Invalid player turn."

        return [COLS * (player_turn % 2) + i for i in range(COLS - 1)
                if self.cells[COLS * (player_turn % 2) + i] == 0]

    def is_move_valid(self, move):
        if move > (self.cells.size - 1) or move < 0 or \
                self.cells[move] == 0 or \
                move == COLS - 1 and self.whose_turn() == 2 or \
                move == 2 * COLS - 1 and self.whose_turn() == 1:
            return False

        return True

    def get_game_result(self):
        seeds = self.get_uncaptured_seeds()

        seeds[1] += self.cells[COLS - 1]
        seeds[2] += self.cells[2 * COLS - 1]

        return seeds[1] - seeds[2]

    def get_uncaptured_seeds(self):
        seeds = {1: 0, 2: 0}

        for i in range(COLS - 1):
            seeds[1] += self.cells[i]
            seeds[2] += self.cells[i + COLS]

        return seeds

    def is_game_over(self):
        seeds = self.get_uncaptured_seeds()

        return True if seeds[1] == 0 or seeds[2] == 0 \
            else False

    def copy(self):
        new_board = Mancala(self.cells)
        new_board.moves_made = self.moves_made
        return new_board
