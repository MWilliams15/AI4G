from Player import Player
import random

class SmartAI(Player):

    def __init__(self, name, token, board):
        self.board = board
        Player.__init__(self, name, token)

    def get_move(self):
        #do some AI magic
        board_tokens = self.board.GetTokenState()

        for win in self.board.GetWinningMoves():
            cell0 = board_tokens[win[0][1]][win[0][0]]
            cell1 = board_tokens[win[1][1]][win[1][0]]
            cell2 = board_tokens[win[2][1]][win[2][0]]

            token_count = 0

            if cell0 == self._token:
                token_count += 1
            if cell1 == self._token:
                token_count += 1
            if cell2 == self._token:
                token_count += 1


            #we must be about to win, make sure we put it in the right spot
            if token_count > 1:
                if cell0 == ' ':
                    move_x = win[0][0]
                    move_y = win[0][1]
                elif cell1 == ' ':
                    move_x = win[1][0]
                    move_y = win[1][1]
                elif cell2 == ' ':
                    move_x = win[2][0]
                    move_y = win[2][1]
                else:
                    move_x = random.randint(0, 2)
                    move_y = random.randint(0, 2)

                 #stop here and return
                return [move_x, move_y, self._token]

        #not the final move - just guess
        move_x = random.randint(0,2)
        move_y = random.randint(0,2)
        return [move_x,move_y,self._token]