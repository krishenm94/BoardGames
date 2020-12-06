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

# tree.train(Mancala(), 2000000)
#
# play_games(100, tree, random, Mancala())
# play_games(100, random, tree, Mancala())

# x_learning = QLearning()
# o_learning = QLearning()
#
#
# neural = QNeural(MSELoss())

#neural.load("./neural_checkpoints/checkpoint_1607248678_200000")
# neural.train(1, Mancala(), Random(), 200000)
# neural.load("./neural_checkpoints/checkpoint_1607242725_100000") # TicTacToe
#play_game(neural, human, Mancala(), True)
# play_games(1000, neural, random, Mancala())
# play_games(1000, neural, minimax)

# play_games(1000, ab_pruning, random, TicTacToe())
# play_games(1000, random, ab_pruning, TicTacToe())
# play_games(100, minimax, ab_pruning, TicTacToe())
# play_games(100, ab_pruning, minimax, TicTacToe())
# play_games(1000, minimax, random, TicTacToe())
# play_games(1000, random, minimax, TicTacToe())
# play_game(minimax, human, TicTacToe(), True)


# play_games(10, minimax, random, Mancala())
# play_games(10, random, minimax, Mancala())
play_games(50, ab_pruning, random, Mancala())
play_games(50, random, ab_pruning, Mancala())


# play_game(human, ab_pruning, Mancala(), True)
# play_game(human, ab_pruning, Mancala(), True)

# neural.games = 0
# neural.train(2)
#
# play_games(1000, neural, random)
# play_games(1000, random, neural)
#
#
# play_games(1000, neural, minimax)
# play_games(1000, minimax, neural)
