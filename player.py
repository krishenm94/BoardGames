class Player(object):
    """docstring for Player"""

    def __init__(self, name):
        super(Player, self).__init__()
        self.turn = 0
        self.name = name
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.games = 0

        self.time_taken = 0

    def set_turn(self, turn):
        assert self.turn >= 1 or self.turn <= 2, f"Invalid turn set: {turn}. Player is designed for 2 player games."

        self.turn = turn

    def move(self, board):
        assert self.turn >= 1 or self.turn <= 2, "Invalid turn set. Player is designed for 2 player games."

        move = self.get_best_move(board)
        board.execute_turn(move)

    def get_best_move(self, board):
        raise NotImplementedError
