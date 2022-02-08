import numpy as np


class Player:

    def setup(self):
        pass

    def play(self, board):
        return np.random.randint(0, board.shape[1])