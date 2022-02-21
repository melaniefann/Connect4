import importlib
import random
import multiprocessing as mp
from queue import Empty
from argparse import ArgumentParser
import sys
import os
from itertools import combinations
from typing import Dict, Iterable, Tuple

import numpy as np

from checks import check_seq
from player import Player

# arrangement of board
'''
0,0 --->0,6
|
|
V
5,0---->5,6
'''

# board is a numpy array
# empty spots are 0s
# Internally:
#   player 1 pieces are +1
#   player 2 pieces are -1
# each player sees their pieces as +1, and their opponent as -1
# the player with 4 pieces in horizontal, vertical, or diagonal alignment wins
# game continues until all 6*7=42 spots are filled
# game is a draw if all spots filled and no player has managed to align 4 pieces
# timed out action implies opponent wins

ROWS = 6
COLUMNS = 7
NUM_CONNECT = 4
TIMEOUT_MOVE = 0.5
TIMEOUT_SETUP = 2.
MAX_INVALID_MOVES = 3


def runner(player_path: str, move_queue: mp.Queue, board_queue: mp.Queue):
    class_name = 'Player'
    try:
        components = player_path.split('/')
        module_name = components[0]
        player_module = importlib.import_module(module_name)
        if len(components) == 2:
            class_name = components[1]
    except Exception as exc:
        print('Could not load player %s due to: %s' % (player_path, exc))
        return -1

    player_cls = getattr(player_module, class_name)
    player: Player = player_cls()
    player.setup()
    move_queue.put('ready')
    while True:
        board = board_queue.get()
        if board is None:
            break
        move = player.play(board)
        move_queue.put(move)


class Connect4Board():

    def __init__(
            self, rows=ROWS, columns=COLUMNS, timeout_move=TIMEOUT_MOVE,
            timeout_setup=TIMEOUT_SETUP, num_connect=NUM_CONNECT,
            max_invalid_moves=MAX_INVALID_MOVES
    ):
        """
        rows : int -- number of rows in the game
        columns : int -- number of columns in the game
        time_out_secs : float -- time in seconds after which other player is declared winner
        """

        # collect max and min player vunetids for logging scores
        self.agents = {}
        self.rows = rows
        self.columns = columns
        self.timeout_move = timeout_move
        self.timeout_setup = timeout_setup
        self.max_invalid_moves = max_invalid_moves

        self.kernels = (
            np.ones((1, num_connect)),
            np.ones((num_connect, 1)),
            np.eye(num_connect),
            np.fliplr(np.eye(num_connect))
        )
        self.reset_board()

    def __str__(self) -> str:
        board = self._board.copy().astype(int)
        return np.array2string(board)

    def reset_board(self):
        self._board = np.zeros((self.rows, self.columns))

    def move_is_valid(self, action):
        if (action < 0) | (action >= self.columns):
            return False
        return self._board[0, action] == 0

    def game_draw(self):
        return 0 not in self._board

    def connected4(self, board: np.ndarray):
        # Check if +1s in the board are connected. So will need to convert
        # player2's -1s first before passing.
        for kernel in self.kernels:
            if check_seq(self.board, kernel):
                return True
        return False

    def update_board(self, col_chosen, value):
        for i in reversed(range(self.rows)):
            # find first empty row
            if self._board[i, col_chosen] == 0:
                # place value
                self._board[i, col_chosen] = value
                break

    def play(self, player1: str, player2: str):

        # Randomly swap p1, p2 for first move.
        toss = random.randint(0, 1)
        p1, p1piece = (player1, +1) if toss == 1 else (player2, -1)
        p2, p2piece = (player2, -1) if toss == 1 else (player1, +1)

        p1_move_queue = mp.Queue(maxsize=1)
        p2_move_queue = mp.Queue(maxsize=1)
        p1_board_queue = mp.Queue(maxsize=1)
        p2_board_queue = mp.Queue(maxsize=1)

        self.reset_board()
        winner, reason, moves = None, '', []
        try:
            p1_process = mp.Process(target=runner, args=(p1, p1_move_queue, p1_board_queue))
            p1_process.start()
            status1 = p1_move_queue.get(timeout=self.timeout_setup)
            if status1 != 'ready': raise Exception(status1)
        except Exception as exc:
            winner, reason = p2, 'Error: %s' % exc
            status1 = ''
        try:
            p2_process = mp.Process(target=runner, args=(p2, p2_move_queue, p2_board_queue))
            p2_process.start()
            status2 = p2_move_queue.get(timeout=self.timeout_setup)
            if status2 != 'ready': raise Exception(status2)
        except Exception as exc:
            if status1 == 'ready':
                winner, reason = p1, 'Error: %s' % exc
            else:
                winner, reason = None, 'Both players\' setup failed'
                status2 = ''

        if reason:
            return winner, reason, moves

        p1_invalid, p2_invalid = 0, 0
        while True:

            p1_board_queue.put(self._board)
            try:
                move = p1_move_queue.get(timeout=self.timeout_move)
                if not self.move_is_valid(move):
                    p1_invalid += 1
                    if p1_invalid >= self.max_invalid_moves:
                        winner, reason = p2, 'Invalid moves exceeded %d' % self.max_invalid_moves
                else:
                    # Player 1's pieces are represented as +1
                    self.update_board(move, p1piece)
                    moves.append(move)
                if self.connected4(self._board):
                    winner, reason = p1, 'Connected 4'
                elif self.game_draw():
                    winner, reason = None, 'Game drawn'
            except Empty:
                winner, reason = p2, 'Move timeout'
            finally:
                if reason: break

            p2_board = self._board * -1  # each player sees their pieces as +1
            p2_board_queue.put(p2_board)
            try:
                move = p2_move_queue.get(timeout=self.timeout_move)
                if not self.move_is_valid(move):
                    p2_invalid += 1
                    if p2_invalid >= self.max_invalid_moves:
                        winner, reason = p1, 'Invalid moves exceeded %d' % self.max_invalid_moves
                else:
                    # Player 2's pieces are represented as -1
                    self.update_board(move, p2piece)
                    moves.append(move)
                if self.connected4(self._board * -1):
                    winner, reason = p2, 'Connected 4'
                elif self.game_draw():
                    winner, reason = None, 'Game drawn'
            except Empty:
                winner, reason = p1, 'Move timeout'
            finally:
                if reason: break

        p1_board_queue.put(None)
        p2_board_queue.put(None)
        p1_process.join()
        p2_process.join()
        return winner, reason, moves

    def play_multiple(
            self, player1: str, player2: str, num: int = 1
    ) -> Dict[str, int]:
        record = {
            player1: 0, player2: 0, None: 0
        }

        for i in range(num):
            winner, reason, moves = self.play(player1, player2)
            record[winner] += 1
        return record

    @property
    def board(self, ):
        return self._board


def championship(
        arena: Iterable[str], game_options: Dict = None, num: int = 1, verbose: bool = True,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, Dict[str, int]]:
    # If arena is a list with a single string, it is assumed to be the path to a directory.
    # The directory should contain python modules or packages. From each of them,
    # a class Player should be able to be imported with the step() and play()
    # methods.
    idx_insertion = None
    if len(arena) == 1:
        idx_insertion = len(sys.path)
        abs_path = os.path.abspath(arena[0])
        sys.path.append(abs_path)
        arena = os.listdir(arena[0])
        arena = [
            # Convert .py files to module names, otherwise assume they are packages
            p[:-3] if p.endswith('.py') else p \
            for p in arena if (
                # Only look at files if they don't start with _, . (like __init)
                    not (p.startswith('.') or p.startswith('_')) and \
                    (p.endswith('.py') or os.path.isdir(os.path.join(abs_path, p)))
            )
        ]
    # Victories is a 2D array, with a row for each player, and each column
    # containing the number of wins against each player. So victories[2,3] will
    # have the number of wins player 2 had over player 3.
    # The dictionary idx_ref maps a player name to its index in `victories`
    # So victories[idx_ref['name']] will return the row of victories for player
    # `name`.
    victories = np.zeros((len(arena), len(arena)), dtype=int)
    losses = np.zeros((len(arena), len(arena)), dtype=int)
    draws = np.zeros((len(arena), len(arena)), dtype=int)
    idx_ref = {player_name: i for i, player_name in enumerate(arena)}
    # If arena was a string, it is now expanded into a list of player names with
    # the default Player class. If it already was a list of strings, those can
    # contain non-default class names like module.submodule/classname.
    # Now generating pairings of players for a game:
    max_len = max(map(len, arena))
    for player1, player2 in (combinations(arena, 2)):
        game = Connect4Board(**game_options)
        record = game.play_multiple(player1, player2, num)
        victories[idx_ref[player1], idx_ref[player2]] += record[player1]
        victories[idx_ref[player2], idx_ref[player1]] += record[player2]
        draws[idx_ref[player1], idx_ref[player2]] += record[None]
        draws[idx_ref[player2], idx_ref[player1]] += record[None]
        if verbose:
            print(f'{player1:>{max_len}} vs {player2:<{max_len}}')
            print(f'{record[player1]:>{max_len}} -- {record[player2]:<{max_len}}')
    losses = victories.T
    if idx_insertion is not None:
        del sys.path[idx_insertion]  # leave sys.path unchanged after function returns
    return victories, losses, draws, idx_ref


if __name__ == '__main__':
    parser = ArgumentParser(
        prog='Connect 4 Game',
        description='Play Connect 4 between two players.')
    parser.add_argument(
        '-v', '--versus', nargs=2, metavar=('P1', 'P2'),
        help=('Play one game between two players. Specify players as '
              '`MODULE.PATH/CLASSNAME` or `MODULE.PATH` where the default `Player` '
              'class is used. For e.g. `dummy/LazyBoi`, or `dummy` (which will '
              'use the `dummy.Player` class.')
    )
    parser.add_argument(
        '-c', '--championship', nargs='+', metavar='DIRECTORY',
        help=('Specify directory containing player modules/packages, OR list '
              'of player modules/packages. Each player plays against every other '
              'player. If directory given, each module/package should implement '
              'the default `Player` class.')
    )
    parser.add_argument(
        '-n', '--num', type=int, default=1,
        help='Number of games to play for a pair in a championship.'
    )
    parser.add_argument(
        '--rows', type=int, default=ROWS,
        help='Number of rows in game board.'
    )
    parser.add_argument(
        '--columns', type=int, default=COLUMNS,
        help='Number of columns in game board.'
    )
    parser.add_argument(
        '--num_connect', type=int, default=NUM_CONNECT,
        help='Number dots connected that constitutes a win. Less than size of board.'
    )
    parser.add_argument(
        '--timeout_move', type=float, default=TIMEOUT_MOVE,
        help='Time alotted per player move.'
    )
    parser.add_argument(
        '--timeout_setup', type=float, default=TIMEOUT_SETUP,
        help='Time alotted for setup before each game.'
    )
    parser.add_argument(
        '--max_invalid_moves', type=int, default=MAX_INVALID_MOVES,
        help='Max invalid moves before forfeiting the game.'
    )
    args = parser.parse_args()

    if args.versus is not None and args.championship is not None:
        print('Only specify either `versus` or `championship` option.', file=sys.stderr)
        exit(-1)

    game_options = dict(
        rows=args.rows, columns=args.columns,
        timeout_move=args.timeout_move, timeout_setup=args.timeout_setup,
        num_connect=args.num_connect,
        max_invalid_moves=args.max_invalid_moves
    )

    if args.versus is not None:
        game = Connect4Board(**game_options)
        winner, reason, moves = game.play(args.versus[0], args.versus[1])
        print('Winner %s, due to %s' % (winner, reason))
        print(game)
    else:
        vic, los, dra, ref = championship(args.championship, game_options, args.num)
        reverse_ref = {idx: name for name, idx in ref.items()}
        max_len = max(map(len, ref.keys()))
        totals = np.sum(vic, axis=1)
        rankings = np.argsort(totals)[::-1]
        print('{:{max_len}s}\t{:2s}'.format('Player', 'Wins', max_len=max_len))
        for idx in rankings:
            print('{:{max_len}s}\t{:2d}'.format(reverse_ref[idx], totals[idx], max_len=max_len))
