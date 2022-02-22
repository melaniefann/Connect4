from player import Player
import numpy as np


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

        raise NotImplementedError()

    def getValidMoves(self, board) -> []:
        validMoves = []
        for i in range(0, board.shape[0]):
            if board[0][i] == 0:
                np.append(validMoves, i)
        return validMoves

    def isTerminalNode(self, board) -> bool:
        pass

    def heuristic(self, board) -> int:
        pass

    def makeNewBoard(self, board, col, value) -> np.ndarray:
        newBoard = board.copy()
        for i in range(board.shape[0], 0, -1):
            if newBoard[i][col] == 0:
                newBoard[i][col] = value
                break
        return newBoard



    def alphabeta(self, board, depth, alpha, beta, maximizingPlayer) -> (int, int):
        validMoves = getValidMoves()
        isTerminal = isTerminalNode(board)
        columnToPlay = None
        if depth == 0 or isTerminal:
            return columnToPlay, heuristic(board)
        if maximizingPlayer:
            bestHeuristic = -10000000
            for column in validMoves:
                newBoard = makeNewBoard(self, board, column, +1)
                curHeuristic = alphabeta(self, newBoard, alpha, beta, False)
                if curHeuristic > bestHeuristic:
                    bestHeuristic = curHeuristic
                    columnToPlay = column

                if value >= beta:
                    break
                alpha = max(alpha, value)
                return columnToPlay, value
        else:
            bestHeuristic = 10000000
            for column in validMoves:
                newBoard = makeNewBoard(self, board, column, -1)
                curHeuristic = alphabeta(self, newBoard, alpha, beta, True)
                if curHeuristic < bestHeuristic:
                    bestHeuristic = curHeuristic
                    columnToPlay = column
                if value <= alpha:
                    break
                beta = min(beta, value)
                return columnToPlay, value
