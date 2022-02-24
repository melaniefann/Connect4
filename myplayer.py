from player import Player as Player
import numpy as np


def make_new_board(board, col, value) -> np.ndarray:
    newBoard = board.copy()
    for i in range(board.shape[0] - 1, 0, -1):
        if newBoard[i][col] == 0:
            newBoard[i][col] = value
            break
    return newBoard


def get_valid_moves(board):
    validMoves = []
    for i in range(0, board.shape[0]):
        if board[0][i] == 0.:
            validMoves.append(i)
    return validMoves


def col_in_range(colNum) -> bool:
    return 0 < colNum < 6


def row_in_range(rowNum) -> bool:
    return 0 < rowNum < 5


def evaluation_function(board) -> int:
    my_win = 0
    opp_win = 0
    my_move = +1
    opp_move = -1

    # horizontal
    for row in range(0, 5):  # for each row
        for startCol in range(0, 3):
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
    for col in range(0, 6):
        for startRow in range(0, 2):
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
    for row in range(0, 2):
        for col in range(0, 3):
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
    for row in range(3, 5):
        for col in range(0, 2):
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
    print('opp_win', opp_win)
    print('my_win', my_win)
    return my_win - opp_win


def is_winning_board(board, column, maximizing) -> bool:
    if maximizing:
        value_to_check = +1
    else:
        value_to_check = -1

    # get the last played row
    i = 5
    while (i > -1):
        if board[i][column] == 0:
            break
        i -= 1
    rowNum = i + 1

    # check horizontal
    for start in range(column - 3, column):
        if col_in_range(start) and col_in_range(start + 3):
            if (board[rowNum, start] == value_to_check
                    and board[rowNum, start + 1] == value_to_check
                    and board[rowNum, start + 2] == value_to_check
                    and board[rowNum, start + 3] == value_to_check):
                return True

    # check vertical
    if row_in_range(rowNum + 3):
        if (board[rowNum, column] == value_to_check
                and board[rowNum + 1, column] == value_to_check
                and board[rowNum + 2, column] == value_to_check
                and board[rowNum + 3, column] == value_to_check):
            return True

    # check down diagonal
    for startRow in range(rowNum - 3, rowNum):
        if row_in_range(startRow) and row_in_range(startRow + 3):
            for startCol in range(column - 3, column):
                if col_in_range(startCol) and col_in_range(startCol + 3):
                    if (board[startRow, startCol] == value_to_check
                            and board[startRow + 1, startCol + 1] == value_to_check
                            and board[startRow + 2, startCol + 2] == value_to_check
                            and board[startRow + 3, startCol + 3] == value_to_check):
                        return True

    # check up diagonal
    for startRow in range(rowNum + 3, rowNum, -1):
        if row_in_range(startRow) and row_in_range(startRow - 3):
            for startCol in range(column - 3, column):
                if col_in_range(startCol) and col_in_range(startCol + 3):
                    print(startRow, startCol)
                    if (board[startRow, startCol] == value_to_check
                            and board[startRow - 1, startCol + 1] == value_to_check
                            and board[startRow - 2, startCol + 2] == value_to_check
                            and board[startRow - 3, startCol + 3] == value_to_check):
                        return True

    return False


def alpha_beta(board, depth, alpha, beta, maximizing, lastColumn):
    won = False
    if lastColumn is not None:
        won = is_winning_board(board, lastColumn, maximizing)
    columnToPlay = None

    if won:
        print("winning")
        if maximizing:
            return [columnToPlay, math.inf]
        else:
            return [columnToPlay, -math.inf]

    validMoves = get_valid_moves(board)

    if depth == 0 or len(validMoves) == 0:
        return [columnToPlay, evaluation_function(board)]

    if maximizing:
        bestHeuristic = -100000000
        for column in validMoves:
            newBoard = make_new_board(board, column, +1)
            curHeuristic = alpha_beta(newBoard, depth - 1, alpha, beta, False, column)[1]
            if curHeuristic > bestHeuristic:
                bestHeuristic = curHeuristic
                columnToPlay = column
            elif curHeuristic == bestHeuristic:
                columnToPlay = random.choice(column, columnToPlay)
            if bestHeuristic >= beta:
                break
            alpha = max(alpha, bestHeuristic)
    else:
        bestHeuristic = 100000000
        for column in validMoves:
            newBoard = make_new_board(board, column, -1)
            curHeuristic = alpha_beta(newBoard, depth - 1, alpha, beta, True, column)[1]
            if curHeuristic < bestHeuristic:
                bestHeuristic = curHeuristic
                columnToPlay = column
            elif curHeuristic == bestHeuristic:
                columnToPlay = random.choice(column, columnToPlay)
            if bestHeuristic <= alpha:
                break
            beta = min(beta, bestHeuristic)
    return [columnToPlay, bestHeuristic]

    # check the most recent piece that was added to the board to see if it wins


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

        return alpha_beta(board, 100, 100000000, -100000000000, True, None)[0]
