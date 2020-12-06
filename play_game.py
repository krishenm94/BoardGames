from board.board import Result

from tqdm import trange
import time


def play_game(x_player, o_player, board, print_board=False):
    x_player.set_turn(1)
    o_player.set_turn(2)

    while not board.is_game_over():
        player = o_player
        if board.whose_turn() == 1:
            player = x_player

        player.move(board)

        if print_board:
            board.print()

    if print_board:
        print(board.get_game_result())

    return board


def play_games(total_games, x_player, o_player, board):
    results = {
        Result.One_Wins: 0,
        Result.Two_Wins: 0,
        Result.Draw: 0
    }

    print("%s as X and %s as O" % (x_player.name, o_player.name), flush=True)
    print("Playing %d games" % total_games, flush=True)

    time.sleep(0.05) # Ensures no collisions between tqdm prints and main prints
    for _ in trange(total_games):
        end_of_game = (play_game(x_player, o_player, board.copy()))
        result = end_of_game.get_game_result()
        if result > 0:
            results[Result.One_Wins] += 1
        elif result < 0:
            results[Result.Two_Wins] += 1
        else:
            results[Result.Draw] += 1

    x_wins_percent = results[Result.One_Wins] / total_games * 100
    o_wins_percent = results[Result.Two_Wins] / total_games * 100
    draw_percent = results[Result.Draw] / total_games * 100

    print(f"Player 1 Wins: {x_wins_percent:.2f}%")
    print(f"Player 2 Wins: {o_wins_percent:.2f}%")
    print(f"Draw  : {draw_percent:.2f}%")
    print("")
