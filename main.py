from random_player import Random
from minimax import Minimax
from play_game import play_game, play_games
from qlearning import QLearning
from mcts import Mcts
from human import Human
from qneural import QNeural
from abpruning import ABPruning
from board.tictactoe import TicTacToe
from torch.nn import MSELoss
from board.mancala import Mancala

human = Human()
tree = Mcts()
minimax = Minimax()
random = Random()
ab_pruning = ABPruning()
# tree.train()

# x_learning = QLearning()
# o_learning = QLearning()
#
#
# neural = QNeural(MSELoss())
#
# neural.train(1)
# play_games(1000, neural, random)
# play_games(1000, neural, minimax)

# play_game(human, ab_pruning)
# play_game(ab_pruning, human)

# play_games(100, ab_pruning, random, TicTacToe())
# play_games(100, random, ab_pruning, TicTacToe())
# play_games(100, minimax, ab_pruning, TicTacToe())
# play_games(100, ab_pruning, minimax, TicTacToe())
# play_games(1000, minimax, random, TicTacToe())
# play_games(1000, random, minimax, TicTacToe())
# play_game(minimax, human, TicTacToe(), True)

play_games(100, minimax, random, Mancala())
play_games(100, random, minimax, Mancala())

# play_game(random, human, Mancala(), True)
# play_game(human, random, Mancala(), True)

# neural.games = 0
# neural.train(2)
#
# play_games(1000, neural, random)
# play_games(1000, random, neural)
#
#
# play_games(1000, neural, minimax)
# play_games(1000, minimax, neural)
