from player import Player
from board.board import Result
from net import *

import torch
from torch import nn
import numpy as np
from time import sleep
from tqdm import trange
from collections import deque
import random
from enum import Enum
import csv
from datetime import datetime
from time import time
from shutil import copyfile

DISCOUNT_FACTOR = 1.0
INITIAL_EPSILON = 0.7
TRAINING_GAMES = 100000

CHECKPOINT_PATH = "./neural_checkpoints/checkpoint_selfplay"
RESULTS_LOG_PATH = './training_results'
CSV = '.csv'


class Key(Enum):
    Net1 = 0,
    Net2 = 7,
    Optimizer1 = 1,
    Optimizer2 = 8,
    Games = 2,
    Wins = 3,
    Draws = 4,
    Losses = 5,
    Time = 6


def time_str():
    return datetime.fromtimestamp(time()).isoformat()


class QNeural(Player):
    """docstring for QNeural"""

    def __init__(self, loss_function):
        super(QNeural, self).__init__("Q Neural Network")

        # print(f"Nets loaded on {cuda.get_device_name(0)}")
        # print(cuda.get_device_properties(0))
        self.online_nets = {1: MancNet(), 2: MancNet()}
        self.target_nets = {1: MancNet(), 2: MancNet()}
        self.update_target_nets()

        self.optimizers = {1: torch.optim.SGD(self.online_nets[1].parameters(), lr=0.1),
                           2: torch.optim.SGD(self.online_nets[2].parameters(), lr=0.1)}

        self.loss_function = loss_function

    def update_target_nets(self):
        for turn in [1, 2]:
            self.target_nets[turn].load_state_dict(self.online_nets[turn].state_dict())
            self.target_nets[turn].eval()

    def get_best_move(self, board):
        return self.choose_move_index(board, 0)

    def get_q_values(self, board, net):
        net_input = torch.tensor(board.cells, dtype=torch.float)
        return net(net_input)

    def filter_output(self, net_output, board):
        valid_moves = board.get_valid_moves(self.turn)
        valid_output_move_pairs = []
        for move in valid_moves:
            valid_output_move_pairs.append((move, net_output[move].item()))
        return valid_output_move_pairs

    def train(self, board, total_games=TRAINING_GAMES):
        total_games = total_games - self.games

        print(f"Training {self.name} for {total_games} games.", flush=True)
        print(f"Starting game number: {self.games}")
        results_filepath = '_'.join([RESULTS_LOG_PATH, str(int(time()))]) + CSV
        copyfile(RESULTS_LOG_PATH + CSV, results_filepath)

        sleep(0.05)  # Ensures no collisions between tqdm prints and main prints
        for game in trange(total_games):
            self.games += 1
            self.play_training_game(board, epsilon)
            # Decrease exploration probability
            if (game + 1) % (total_games / 20) == 0:
                epsilon = max(0, epsilon - 0.05)
                # tqdm.write(f"{game + 1}/{total_games} games, using epsilon={epsilon}...")

            if (game + 1) % 10000 == 0:
                self.save()

            if (game + 1) % 1000 == 0:
                self.record(results_filepath)

            if (game + 1) % 10 == 0:
                self.target_net.load_state_dict(self.online_net.state_dict())
                self.target_net.eval()

    def record(self, path):
        with open(path, mode='a', newline='') as file:
            file_writer = csv.writer(file, delimiter=',')
            file_writer.writerow([time_str(), self.games, self.wins, self.draws, self.losses])

    def save(self):
        torch.save({Key.Time.name: time_str(),
                    Key.Games.name: self.games,
                    Key.Wins.name: self.wins,
                    Key.Draws.name: self.draws,
                    Key.Losses.name: self.losses,
                    Key.Net.name: self.online_net.state_dict(),
                    Key.Optimizer.name: self.optimizer.state_dict()},
                   '_'.join([CHECKPOINT_PATH, str(int(time())), str(self.games)]))

    def play_training_game(self, board, epsilon):
        move_history = deque()

        while not board.is_game_over():
            board = self.play_training_move(board, epsilon, move_history)

        self.post_training_game_update(board, move_history)

    def play_training_move(self, board, epsilon, move_history):
        move = self.choose_move_index(board, epsilon)
        move_history.appendleft((board, move))
        return board.simulate_turn(move)

    def choose_move_index(self, board, epsilon):
        if epsilon > 0:
            random_value_from_0_to_1 = np.random.uniform()
            if random_value_from_0_to_1 < epsilon:
                return random.choice(board.get_valid_moves(self.turn))

        net_output = self.get_q_values(board, self.online_nets[board.whose_turn()])
        valid_move_value_pairs = self.filter_output(net_output, board)

        return max(valid_move_value_pairs, key=lambda pair: pair[1])[0]

    def post_training_game_update(self, board, move_history):
        end_state_value = self.get_end_state_value(board)

        # Initial loss update
        next_board, move = move_history[0]
        self.backpropagate(next_board, move, end_state_value)

        for board, move in list(move_history)[1:]:
            with torch.no_grad():
                # next_q_values = self.get_q_values(next_board, self.online_net) # QN
                next_q_values = self.get_q_values(next_board, self.target_net)  # Double QN
                max_next_q_value = torch.max(next_q_values).item()

            self.backpropagate(board, move, max_next_q_value * DISCOUNT_FACTOR)
            next_board = board

    def backpropagate(self, board, turn, move, target_value):
        self.optimizers[turn].zero_grad()

        board_tensor = torch.tensor(board.cells, dtype=torch.float)
        output = self.online_nets[turn](board_tensor)

        target_output = output.clone().detach()
        target_output[move] = target_value
        for move in board.get_invalid_moves(turn):
            target_output[move] = 0

        loss = self.loss_function(output, target_output)
        loss.backward()

        self.optimizers[turn].step()

    def get_end_state_value(self, board):
        assert board.is_game_over(), "Game is not over"

        game_result = board.get_game_result()

        if game_result == Result.Draw:
            self.draws += 1
            return 1

        if game_result > 0:
            result = 1 if self.turn == 1 else 0
        elif game_result < 0:
            result = 1 if self.turn == 2 else 0

        if result == 1:
            self.wins += 1
        else:
            self.losses += 1

        return result

    def load(self, path):
        loaded_checkpoint = torch.load(path)

        self.online_nets[1].load_state_dict(loaded_checkpoint[Key.Net1.name])
        self.online_nets[2].load_state_dict(loaded_checkpoint[Key.Net2.name])

        self.update_target_nets()

        self.optimizers[1].load_state_dict(loaded_checkpoint[Key.Optimizer1.name])
        self.optimizers[2].load_state_dict(loaded_checkpoint[Key.Optimizer2.name])

        self.games = loaded_checkpoint[Key.Games.name]
        self.wins = loaded_checkpoint[Key.Wins.name]
        self.draws = loaded_checkpoint[Key.Draws.name]
        self.losses = loaded_checkpoint[Key.Losses.name]
