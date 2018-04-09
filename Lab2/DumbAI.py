from Player import Player
import random

class DumbAI(Player):

    def __init__(self, name, token):
        Player.__init__(self, name, token)

    def get_move(self):
        move_x = random.randint(0,2)
        move_y = random.randint(0,2)

        return [move_x,move_y,self._token]