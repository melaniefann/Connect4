import time
import random

import numpy as np

from player import Player as P



class LazyBoi(P):


    def setup(self):
        time.sleep(1.)
        print(self.__class__.__name__ + ': ...Hmm?')


    def play(self, board: np.ndarray) -> int:
        time.sleep(random.random() + 0.2)
        return 0



class OffBase(P):

    def setup(self):
        print(self.__class__.__name__ + ': Umm...this is the swing dance class, right?')


    def play(self, board: np.ndarray) -> int:
        return random.randint(board.shape[1], board.shape[1] + 5)



#  We dont need to inherit from `player.Player` as long as the two methods are
# implemented.
class SeeWhatSticks:


    def setup(self):
        print(self.__class__.__name__ + ': Bruh I "See What Sticks", I don\'t need to prepare -_-')


    def play(self, board: np.ndarray) -> int:
        return random.randint(0, board.shape[1]-1)



# This is the default player. If the player class is not specified in the script
# argument, the class named `Player` is imported.
class Player(P):


    def setup(self):
        print(self.__class__.__name__ + ': The default imported class name. Pretty boring.')


    def play(self, board: np.ndarray) -> int:
        return 0



if __name__=='__main__':
    from connect4 import Connect4Board

    print('Playing 2 dummy players against each other')
    game = Connect4Board()

    p1 = 'dummies/LazyBoi'
    p2 = 'dummies/SeeWhatSticks'
    winner, reason, moves = game.play(p1, p2)
    print('Winner: %s' % winner)
    print('Reason: %s' % reason)
    print(game)