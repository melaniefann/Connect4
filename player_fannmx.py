import numpy as np
import random

ROWS = 6
COLS = 7
DEPTH = 3


def make_new_board(board, col, value) -> np.ndarray:
    """
    makes a copy of the board to be used in the alpha-beta search with the inserted value at column col
    """
    newBoard = board.copy()
    for i in range(5, -1, -1):
        if newBoard[i][col] == 0:
            newBoard[i, col] = value
            break
    return newBoard


def get_valid_moves(board):
    """
    returns an array of valid moves (columns)
    """
    validMoves = []
    for i in range(0, COLS):
        if board[0][i] == 0:
            validMoves.append(i)
    return validMoves


def is_winning_board(board) -> int:
    """
    returns the player's value that won or 0 if no one has one
    """

    # horizontal
    for row in range(0, 6):  # for each row
        for startCol in range(0, 4):
            firstPiece = board[row, startCol]
            if firstPiece != 0:
                if ((board[row, startCol + 1] == firstPiece)
                        and (board[row, startCol + 2] == firstPiece)
                        and (board[row, startCol + 3] == firstPiece)):
                    return firstPiece

    # vertical
    for col in range(0, 7):
        for startRow in range(0, 3):
            firstPiece = board[startRow, col]
            if firstPiece != 0:
                if ((board[startRow + 1, col] == firstPiece)
                        and (board[startRow + 2, col] == firstPiece)
                        and (board[startRow + 3, col] == firstPiece)):
                    return firstPiece

    # down diagonals
    for row in range(0, 3):
        for col in range(0, 4):
            firstPiece = board[row, col]
            if firstPiece != 0:
                if ((board[row + 1][col + 1] == firstPiece)
                        and (board[row + 2][col + 2] == firstPiece)
                        and (board[row + 3][col + 3] == firstPiece)):
                    return firstPiece

    # up diagonals
    for row in range(3, 6):
        for col in range(0, 3):
            firstPiece = board[row, col]
            if firstPiece != 0:
                if ((board[row - 1][col + 1] == firstPiece)
                        and (board[row - 2][col + 2] == firstPiece)
                        and (board[row - 3][col + 3] == firstPiece)):
                    return firstPiece
    return 0


def canBlockOrWinMove(board, move) -> int:
    """
    determines if we can block a winning move; if so, returns column to play to block move
    """

    for row in range(0, 6):  # for each row
        for startCol in range(0, 4):
            if row != 0:
                if ((board[row, startCol] == move)
                        and (board[row, startCol + 1] == move)
                        and (board[row, startCol + 2] == move)
                        and (board[row, startCol + 3] == 0)
                        and (board[row - 1, startCol + 3] != 0)):
                    return startCol + 3
                elif ((board[row, startCol] == 0)
                      and (board[row, startCol + 1] == move)
                      and (board[row, startCol + 2] == move)
                      and (board[row, startCol + 3] == move)
                      and (board[row - 1, startCol] != 0)):
                    return startCol
                elif ((board[row, startCol] == move)
                      and (board[row, startCol + 1] == 0)
                      and (board[row, startCol + 2] == move)
                      and (board[row, startCol + 3] == move)
                      and (board[row - 1, startCol + 1] != 0)):
                    return startCol + 1
                elif ((board[row, startCol] == move)
                      and (board[row, startCol + 1] == move)
                      and (board[row, startCol + 2] == 0)
                      and (board[row, startCol + 3] == move)
                      and (board[row - 1, startCol + 2] != 0)):
                    return startCol + 2
            else:
                if ((board[row, startCol] == move)
                        and (board[row, startCol + 1] == move)
                        and (board[row, startCol + 2] == move)
                        and (board[row, startCol + 3] == 0)):
                    return startCol + 3
                elif ((board[row, startCol] == 0)
                      and (board[row, startCol + 1] == move)
                      and (board[row, startCol + 2] == move)
                      and (board[row, startCol + 3] == move)):
                    return startCol
                elif ((board[row, startCol] == move)
                      and (board[row, startCol + 1] == 0)
                      and (board[row, startCol + 2] == move)
                      and (board[row, startCol + 3] == move)):
                    return startCol + 1
                elif ((board[row, startCol] == move)
                      and (board[row, startCol + 1] == move)
                      and (board[row, startCol + 2] == 0)
                      and (board[row, startCol + 3] == move)):
                    return startCol + 2

    for col in range(0, 7):  # check columns
        for startRow in range(0, 3):
            if ((board[startRow, col] == move)
                    and (board[startRow + 1, col] == move)
                    and (board[startRow + 2, col] == move)
                    and (board[startRow + 3, col] == 0)):
                return col

    for row in range(0, 3):  # down diagonals
        for col in range(0, 4):
            if ((board[row][col] == move)
                    and (board[row + 1][col + 1] == move)
                    and (board[row + 2][col + 2] == move)
                    and (board[row + 3][col + 3] == 0)
                    and (board[row + 2][col + 3] != 0)):
                return col + 3
            elif ((board[row][col] == move)
                  and (board[row + 1][col + 1] == move)
                  and (board[row + 2][col + 2] == 0)
                  and (board[row + 3][col + 3] == move)
                  and (board[row + 1][col + 2] != 0)):
                return col + 2
            elif ((board[row][col] == move)
                  and (board[row + 1][col + 1] == 0)
                  and (board[row + 2][col + 2] == move)
                  and (board[row + 3][col + 3] == move)
                  and (board[row][col + 1] != 0)):
                return col + 1
            elif ((board[row][col] == 0)
                  and (board[row + 1][col + 1] == move)
                  and (board[row + 2][col + 2] == move)
                  and (board[row + 3][col + 3] == move)
                  and (row == 0 or board[row - 1][col] != 0)):
                return col

    for row in range(3, 6):  # up diagonals
        for col in range(0, 3):
            if ((board[row][col] == move)
                    and (board[row - 1][col + 1] == move)
                    and (board[row - 2][col + 2] == move)
                    and (board[row - 3][col + 3] == 0)
                    and (row == 0 or board[row - 4][col + 3] != 0)):
                return col + 3
            elif ((board[row][col] == move)
                  and (board[row - 1][col + 1] == move)
                  and (board[row - 2][col + 2] == 0)
                  and (board[row - 3][col + 3] == move)
                  and (board[row - 3][col + 2] != 0)):
                return col + 2
            elif ((board[row][col] == move)
                  and (board[row - 1][col + 1] == 0)
                  and (board[row - 2][col + 2] == move)
                  and (board[row - 3][col + 3] == move)
                  and (board[row - 2][col + 1] != 0)):
                return col + 1
            elif ((board[row][col] == 0)
                  and (board[row - 1][col + 1] == move)
                  and (board[row - 2][col + 2] == move)
                  and (board[row - 3][col + 3] == move)
                  and (board[row - 1][col] != 0)):
                return col
    return -1


def evaluation(board) -> int:
    """
    creates the evaluation function
    - counts the number of possible ways the player can win - the number of possible ways the opponent can win
    """
    my_win = 0
    opp_win = 0

    my_move = +1
    opp_move = -1

    # horizontal
    for row in range(0, 6):  # for each row
        for startCol in range(0, 4):
            if ((board[row, startCol] == opp_move or board[row, startCol] == 0)
                    and (board[row, startCol + 1] == opp_move or board[row, startCol + 1] == 0)
                    and (board[row, startCol + 2] == opp_move or board[row, startCol + 2] == 0)
                    and (board[row, startCol + 3] == opp_move or board[row, startCol + 3] == 0)):
                opp_win += 1
            if ((board[row, startCol] == my_move or board[row, startCol] == 0)
                    and (board[row, startCol + 1] == my_move or board[row, startCol + 1] == 0)
                    and (board[row, startCol + 2] == my_move or board[row, startCol + 2] == 0)
                    and (board[row, startCol + 3] == my_move or board[row, startCol + 3] == 0)):
                my_win += 1

    # vertical
    for col in range(0, 7):
        for startRow in range(0, 3):
            if ((board[startRow, col] == opp_move or board[startRow, col] == 0)
                    and (board[startRow + 1, col] == opp_move or board[startRow + 1, col] == 0)
                    and (board[startRow + 2, col] == opp_move or board[startRow + 2, col] == 0)
                    and (board[startRow + 3, col] == opp_move or board[startRow + 3, col] == 0)):
                opp_win += 1
            if ((board[startRow, col] == my_move or board[startRow, col] == 0)
                    and (board[startRow + 1, col] == my_move or board[startRow + 1, col] == 0)
                    and (board[startRow + 2, col] == my_move or board[startRow + 2, col] == 0)
                    and (board[startRow + 3, col] == my_move or board[startRow + 3, col] == 0)):
                my_win += 1

    # down diagonals
    for row in range(0, 3):
        for col in range(0, 4):
            if ((board[row][col] == opp_move or board[row][col] == 0)
                    and (board[row + 1][col + 1] == opp_move or board[row + 1][col + 1] == 0)
                    and (board[row + 2][col + 2] == opp_move or board[row + 2][col + 2] == 0)
                    and (board[row + 3][col + 3] == opp_move or board[row + 3][col + 3] == 0)):
                opp_win += 1
            if ((board[row][col] == my_move or board[row][col] == 0)
                    and (board[row + 1][col + 1] == my_move or board[row + 1][col + 1] == 0)
                    and (board[row + 2][col + 2] == my_move or board[row + 2][col + 2] == 0)
                    and (board[row + 3][col + 3] == my_move or board[row + 3][col + 3] == 0)):
                my_win += 1

    # up diagonals
    for row in range(3, 6):
        for col in range(0, 3):
            if ((board[row][col] == opp_move or board[row][col] == 0)
                    and (board[row - 1][col + 1] == opp_move or board[row - 1][col + 1] == 0)
                    and (board[row - 2][col + 2] == opp_move or board[row - 2][col + 2] == 0)
                    and (board[row - 3][col + 3] == opp_move or board[row - 3][col + 3] == 0)):
                opp_win += 1
            if ((board[row][col] == my_move or board[row][col] == 0)
                    and (board[row - 1][col + 1] == my_move or board[row - 1][col + 1] == 0)
                    and (board[row - 2][col + 2] == my_move or board[row - 2][col + 2] == 0)
                    and (board[row - 3][col + 3] == my_move or board[row - 3][col + 3] == 0)):
                my_win += 1
    return my_win - opp_win


def alpha_beta(board, depth, alpha, beta, maximizing) -> (int, int):
    """
    performs alpha-beta search
    """
    won = is_winning_board(board)
    valid_moves = get_valid_moves(board)
    column_to_play = None
    if len(valid_moves) > 0:
        column_to_play = random.choice(valid_moves)

    # if it's a terminal node
    if won == -1:
        return [column_to_play, -1000]
    elif won == +1:
        return [column_to_play, +1000]

    valid_moves = get_valid_moves(board)

    if depth == 0 or len(valid_moves) == 0:
        return [column_to_play, evaluation(board)]

    # if it's not a terminal node
    if maximizing:
        bestHeuristic = -1000
        for column in valid_moves:
            newBoard = make_new_board(board, column, +1)
            curHeuristic = alpha_beta(newBoard, depth - 1, alpha, beta, False)[1]
            if curHeuristic > bestHeuristic:
                bestHeuristic = curHeuristic
                column_to_play = column
            alpha = max(alpha, bestHeuristic)
            if alpha >= beta:
                break
        return [column_to_play, bestHeuristic]
    else:
        bestHeuristic = 1000
        for column in valid_moves:
            newBoard = make_new_board(board, column, -1)
            curHeuristic = alpha_beta(newBoard, depth - 1, alpha, beta, True)[1]
            if curHeuristic < bestHeuristic:
                bestHeuristic = curHeuristic
                column_to_play = column
            beta = min(beta, bestHeuristic)
            if beta <= alpha:
                break
        return [column_to_play, bestHeuristic]


class Player:

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
        if board[ROWS - 1][3] == 0:  # always play middle for first move
            return 3

        strategyMove = canBlockOrWinMove(board, +1)
        if strategyMove >= 0:
            return strategyMove

        strategyMove = canBlockOrWinMove(board, -1)
        if strategyMove >= 0:
            return strategyMove

        return alpha_beta(board, DEPTH, -1000, 1000, True)[0]
