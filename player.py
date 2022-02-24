import numpy as np


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
        return np.random.randint(0, 6)


__all__ = ['Player']
