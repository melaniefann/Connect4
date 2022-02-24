from connect4 import Connect4Board
from myplayer import MyPlayer as Player

game = Connect4Board()

# See above on how to sppecify player names as strings.
winner, reason, moves = game.play('myplayer/MyPlayer','myplayer/MyPlayer')

print(game)