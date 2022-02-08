Connect 4 Game

![Game Animation](https://upload.wikimedia.org/wikipedia/commons/a/ad/Connect_Four.gif)

This repository contains code for the [Connect 4][1] game. It provides the interface for each player to program game logic, and then for players to be pitted against each other. There are two kinds of matches:

1. A 1v1 versus match, or
2. a round-robin championship where each player faces off against every other player, and the winner is the one with the most victories.

## Rules

1. The board is a 6-row, 7-column grid erected vertically.
2. Each column is a shaft, such that a piece dropped in a column will fall to the bottom (or on top of the previous piece.)
3. Players take turns choosing which column to drop their piece in.
4. The objective of the game is to drop pieces such that and 4 of your pieces are connected horizintally, vertically, or diagonally first.
5. If there are no more empty spots left, and no player has connected 4 of their pieces, the game is a draw.

## Installing

The code requires `python=3.9 numpy tqdm`. You can `pip install` or `conda install` these packages. It is recommended to use a virtual environment.

## Interface

This repository provides the `Player` class which includes their game logic. It is in turn used by the `Connect4Board` class to run the game.

The `Player` class has two methods which may be overridden:

1. `setup()` is called at the beginning of the game, and may be used to set up any game logic (loading stuff etc.). It is a timed method, and taking too long will cause the player to lose by default.
2. `play(self, board: np.ndarray) -> int` takes the current state of the board, and returns the column index to put the piece in. If the move is invalid, the player loses by default. A move is invalid if the column index is out of bounds, or if the column has no more space left.

When writing up your player, you may subclass the `Player` class, or write your own, but with these method signatures.

The `Connect4Board` class plays matches between two players. It has the `play(p1, p2) -> str, str, list[int]` method that returns the winner, reason for win, and the list of moves as a list of column indices.

`player1`, `player2` are the string names of the modules containing the player object.

* If you have your own `Player` class in a file `myplayer.py` in the working directory, you can simply pass `myplayer`.
* If your player is named something else, then specify the class name like `myplayer/Playa`
* If the player is in a nested module. For example if you'd need to write `from players.simple import Dumbo`, then specify the player as `players.simple/Dumbo`.

## Testing your player

First, write your player code. You can either:

1. Edit the definition in the [`player.py`][2] file
2. Make a new python module and implement the `Player` interface. You can implement different players and test them against each other yourself.

```python
import numpy as np

from player import Player as BasePlayer


# The class named Player will be imported as default, unless another class name
# is provided as part of the argument to Connect4Board.play()
class Player(BasePlayer):
    def setup():
        print('setting up')
    def play(board):
        print(
            'board is a numpy array: %s or shape %s' % \
            (isinstance(board, np.ndarray, board.shape))
        )
        # must return a valid column index
        return 1


# When using the script, if a class name is not provided, by default only
# the class named `Player` will be imported, one per module.
class AnotherPlayer(BasePlayer):
    def setup():
        pass
    def play(board):
        pass

# The class does not need to inherit from the player.Player class, as long as 
# the two methods are implemented.
class StrongIndependentPlayer:
    def setup():
        pass
    def play(board: np.ndarray) -> int:
        return 3
```

There are several ways to test play.

### Using the `Connect4Board` class

```python
from connect4 import Connect4Board

game = Connect4Board()

# See above on how to sppecify player names as strings.
winner, reason, moves = game.play(Player1, Player2)

print(game)
```

### Using the script

```bash
> python connect4.py --help

usage: Connect 4 Game [-h] [-v P1 P2] [-c DIRECTORY [DIRECTORY ...]]

Play Connect 4 between two players.

optional arguments:
  -h, --help            show this help message and exit
  -v P1 P2, --versus P1 P2
                        Play one game between two players. Specify players as `MODULE.PATH/CLASSNAME` or `MODULE.PATH` where the default `Player` class is used. For e.g.   
                        `dummy/LazyBoi`, or `dummy` (which will use the `dummy.Player` class.
  -c DIRECTORY [DIRECTORY ...], --championship DIRECTORY [DIRECTORY ...]
                        Specify directory containing player modules/packages, OR list of player modules/packages. Each player plays against every other player. If directory
                        given, each module/package should implement the default `Player` class.
  -n NUM, --num NUM     Number of games to play for a pair in a championship.
  --rows ROWS           Number of rows in game board.
  --columns COLUMNS     Number of columns in game board.
  --num_connect NUM_CONNECT
                        Number dots connected that constitutes a win. Less than size of board.
  --timeout_move TIMEOUT_MOVE
                        Time alotted per player move.
  --timeout_setup TIMEOUT_SETUP
                        Time alotted for setup before each game.
  --max_invalid_moves MAX_INVALID_MOVES
                        Max invalid moves before forfeiting the game.

# Championships

> python connect4.py -c player_arena

> python connect4.py -c dummies/LazyBoi player_arena.player_vunetid_b dummies/SeeWhatSticks

# Versus games

> python connect4.py -v dummies/LazyBoi player_arena.player_vunetid_a

> python connect4.py -v dummies/LazyBoi dummies

```

[1]: https://en.wikipedia.org/wiki/Connect_Four
[2]: /player.py