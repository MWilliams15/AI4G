from Player import Player


class HumanPlayer(Player):

    def __init__(self, name, token):
        Player.__init__(self, name, token)

    def get_move(self):

        try:
            move_x = int(input("Enter x-coordinate:"))
            move_y = int(input("Enter y-coordinate:"))
        except:
            move_x = -1
            move_y = -1


        return [move_x,move_y,self._token]