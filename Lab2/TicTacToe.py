from Board import GameBoard
from HumanPlayer import HumanPlayer
from DumbAI import DumbAI
from SmartAI import SmartAI

# draw board
# while not game finished
# get player move
# redraw board
# check for game over

board = GameBoard()
player1 = SmartAI("SmartAI", 'O', board)
player2 = DumbAI("DumbAI", 'X')

players = [player1, player2]

for i in range(0, 100):
    print(i)
    board.reset()
    while board.game_over() == 0:
        for player in players:
            move = player.get_move()

            while board.submit_move(move) != 1:
                move = player.get_move()

            if board.game_over() != 0:
                if board.game_over() != 'TIE':
                    player.Winner()
                break


for player in players:
    print("{} won {} times".format(player.get_name(),str(player.GetWinCount())))