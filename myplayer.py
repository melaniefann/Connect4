from player import Player
import numpy as np

ROW = board.shape[0]
COLUMN = board.shape[1]


def row_in_range(rowNum) -> bool:
    return rowNum < 0 or rowNum > 5


def col_in_range(colNum) -> bool:
    return colNum < 0 or colNum > 6


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


def is_winning_board(board, column, maximizing) -> bool:
    value_to_check = None
    if maximizing:
        value_to_check = +1
    else:
        value_to_check = -1
    rowNum = None

    # get the last played location
    for i in range(0, ROW):
        if board[i][column] == 0:
            rowNum = i - 1
            break

    # check horizontal
    for start in range(column - 3, column):
        if col_in_range(start) and col_in_range(start + 3):
            if (board[rowNum, start] == value_to_check
                    and board[rowNum, start + 1] == value_to_check
                    and board[rowNum, start + 2] == value_to_check
                    and board[rowNum, start + 3] == value_to_check):
                return true

    # check vertical
    if row_in_range(rowNum + 3):
        if (board[rowNum, column] == value_to_check
                and board[rowNum + 1, column] == value_to_check
                and board[rowNum + 2, column] == value_to_check
                and board[rowNum + 3, column] == value_to_check):
            return true

    # check down diagonal
    for startRow in range(rowNum - 3, rowNum):
        if row_in_range(startRow) and row_in_range(startRow + 3):
            for startCol in range(column - 3, column):
                if col_in_range(startCol) and col_in_range(startCol + 3):
                    if (board[startRow, startCol] == value_to_check
                            and board[startRow + 1, startCol + 1] == value_to_check
                            and board[startRow + 2, startCol + 2] == value_to_check
                            and board[startRow + 3, startCol + 3] == value_to_check):
                        return true

    # check up diagonal
    for startRow in range(rowNum + 3, rowNum, -1):
        if row_in_range(startRow) and row_in_range(startRow - 3):
            for startCol in range(column - 3, column):
                if col_in_range(startCol) and col_in_range(startCol + 3):
                    if (board[startRow, startCol] == value_to_check
                            and board[startRow - 1, startCol + 1] == value_to_check
                            and board[startRow - 2, startCol + 2] == value_to_check
                            and board[startRow - 3, startCol + 3] == value_to_check):
                        return true

    return false


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
        return alpha_beta(self, board, 10, math.inf, -math.inf, True, None)[0]

    # check the most recent piece that was added to the board to see if it wins

    def heuristic(self, board, maximizing) -> int:
        value_to_add = 0
        value_to_subtract = 0
        value_to_count = None

        if maximizing:
            value_to_count = +1
        else:
            value_to_count = -1


        # needs to check all of them *****
        # horizontal

        # vertical

        # diagonals only need to check from row 5 to 3 as start points
        # right diagonals

        # left diagonals
        pass

    def alpha_beta(self, board, depth, alpha, beta, maximizing, lastColumn) -> (int, int):
        won = is_winning_board(board, lastColumn, maximizing)
        columnToPlay = None

        if won:
            if maximizing:
                return columnToPlay, math.inf
            else:
                return columnToPlay, -math.inf

        validMoves = get_valid_moves(board)

        if depth == 0 or len(validMoves) == 0:
            return columnToPlay, heuristic(self, board, maximizing)

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
