from player import Player
from cache import Cache1, IDENTITY
from math import inf
import time

LOOKAHEAD_LIMIT = 10

class ABPruning(Player):
    """docstring for ABPruning"""

    def __init__(self):
        super(ABPruning, self).__init__("ABPruning")
        self.cache = Cache1(IDENTITY)

    def get_best_move(self, board):
        move_value_pairs = self.get_move_values(board)

        return self.filter(board, move_value_pairs)

    def filter(self, board, move_value_pairs):
        min_or_max = self.min_or_max(board)
        move, value = min_or_max(move_value_pairs, key=lambda pair: pair[1])
        return move

    def get_move_values(self, board):
        moves = board.get_valid_moves(self.turn)
        assert moves, "No valid moves"

        return [(move, self.get_move_value(move, board, -inf, inf, 0))
                for move in moves]

    def get_move_value(self, move, board, alpha, beta, lookup):
        new_board = board.simulate_turn(move)
        cached, found = self.cache.get(new_board)

        if found:
            return cached

        value = self.calculate_position_value(new_board, alpha, beta, lookup)
        self.cache.set(new_board, value)
        return value

    def calculate_position_value(self, board, alpha, beta, lookup):
        if board.is_game_over() or lookup >= LOOKAHEAD_LIMIT:
            return board.get_game_result()
        lookup += 1

        moves = board.get_valid_moves(self.turn)

        min_or_max = self.min_or_max(board)

        value = self.get_move_value(moves[0], board, alpha, beta, lookup)
        for move in moves:
            value = min_or_max(value, self.get_move_value(move, board, alpha, beta, lookup))
            if min_or_max is max:
                alpha = max(alpha, value)
                if alpha >= beta:
                    return value
            else:
                beta = min(beta, value)
                if beta <= alpha:
                    return value

        return value

    def min_or_max(self, board):
        return min if board.moves_made % 2 == 1 else max
