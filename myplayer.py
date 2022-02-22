from player import Player
import numpy as np


def get_valid_moves(board) -> []:
    validMoves = []
    for i in range(0, board.shape[0]):
        if board[0][i] == 0:
            np.append(validMoves, i)
    return validMoves


def make_new_board(board, col, value) -> np.ndarray:
    newBoard = board.copy()
    for i in range(board.shape[0], 0, -1):
        if newBoard[i][col] == 0:
            newBoard[i][col] = value
            break
    return newBoard


class MyPlayer(Player):
    def setup(self):
        """
        This method will be called once at the beginning of the game so the player
        can conduct any setup before the move timer begins. The setup method is
        also timed.
        """

        pass

    def play(self, board: np.ndarray) -> int:
        """
        Given a 2D array representing the game board, return the column index
        in which to place your piece.

        Parameters
        ----------
        board : np.ndarray
            A 2D array where 0s represent empty slots, +1s represent your pieces,
            and -1s represent the opposing player's pieces.

                `index   0   1   2   . column` \\
                `--------------------------` \\
                `0   |   0.  0.  0.  top` \\
                `1   |   -1  0.  0.  .` \\
                `2   |   +1  -1  -1  .` \\
                `.   |   -1  +1  +1  .` \\
                `row |   left        bottom/right`

        Returns
        -------
        int
            The column index in which to place your piece. The piece will drop
            to the lowest empty row in the column (like a pile).
        """

        return alpha_beta(self, board, 10, math.inf, -math.inf, True, None)

    def is_winning_board(self, board, column) -> bool:
        # check the most recent piece that was added to the board to see if it wins
        pass

    def heuristic(self, board) -> int:
        # needs to check all of them *****
        # horizontal

        # vertical

        # right diagonals

        # left diagonals
        pass

    def alpha_beta(self, board, depth, alpha, beta, maximizing, lastColumn) -> (int, int):
        won = is_winning_board(board, lastColumn)
        columnToPlay = None

        if won:
            if maximizing: # need to check this
                return columnToPlay, math.inf
            else:
                return columnToPlay, -math.inf

        validMoves = get_valid_moves(board)
        if depth == 0 or len(validMoves) == 0:
            return columnToPlay, heuristic(board)
        if maximizing:
            bestHeuristic = -math.inf
            for column in validMoves:
                newBoard = make_new_board(board, column, +1)
                curHeuristic = alpha_beta(self, newBoard, alpha, beta, False, column)[1]
                if curHeuristic > bestHeuristic:
                    bestHeuristic = curHeuristic
                    columnToPlay = column
                if value >= beta:
                    break
                alpha = max(alpha, value)
                return columnToPlay, value
        else:
            bestHeuristic = math.inf
            for column in validMoves:
                newBoard = make_new_board(board, column, -1)
                curHeuristic = alpha_beta(self, newBoard, alpha, beta, True, column)[1]
                if curHeuristic < bestHeuristic:
                    bestHeuristic = curHeuristic
                    columnToPlay = column
                if value <= alpha:
                    break
                beta = min(beta, value)
                return columnToPlay, value
