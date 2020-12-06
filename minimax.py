from player import Player
from cache import Cache1, IDENTITY

LOOKAHEAD_LIMIT = 10


class Minimax(Player):
    """docstring for Minimax"""

    def __init__(self):
        super(Minimax, self).__init__("Minimax")
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

        return [(move, self.get_move_value(move, board, 0))
                for move in moves]

    def get_move_value(self, move, board, lookahead):
        new_board = board.simulate_turn(move)
        cached, found = self.cache.get(new_board)

        if found:
            return cached

        value = self.calculate_position_value(new_board, lookahead)
        self.cache.set(new_board, value)

        return value

    def calculate_position_value(self, board, lookahead):
        if board.is_game_over() or lookahead >= LOOKAHEAD_LIMIT:
            return board.get_game_result()
        lookahead += 1

        moves = board.get_valid_moves(self.turn)

        min_or_max = self.min_or_max(board)

        move_values = [self.get_move_value(move, board, lookahead)
                       for move in moves]

        return min_or_max(move_values)

    def min_or_max(self, board):
        return min if board.moves_made % 2 == 1 else max
