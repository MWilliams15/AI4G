class GameBoard:
    __board_tokens = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    __WIN = [[[0, 0], [0, 1], [0, 2]], [[1, 0], [1, 1], [1, 2]], [[2, 0], [2, 1], [2, 2]], [[0, 0], [1, 0], [2, 0]],
             [[0, 1], [1, 1], [2, 1]], [[0, 2], [1, 2], [2, 2]], [[0, 0], [1, 1], [2, 2]], [[2, 0], [1, 1], [0, 2]]]
    __number_of_tokens = 0
    __game_over = 0
    __board = """     |     |      
  {0,0}  |  {1,0}  |  {2,0}   
_____|_____|_____ 
     |     |       
  {0,1}  |  {1,1}  |  {2,1}   
_____|_____|_____ 
     |     |      
  {0,2}  |  {1,2}  |  {2,2}   
     |     |      """

    def __init__(self):
        self.reset()
        self.show_board()

    def game_over(self):
        return self.__game_over

    def reset(self):
        self.__board_tokens = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.__number_of_tokens = 0
        self.__game_over = 0

    def show_board(self):
        new_board = self.__board

        for i in range(0, 3):
            for j in range(0, 3):
                replace_string = "{" + str(j) + ',' + str(i) + '}'
                new_board = new_board.replace(replace_string, self.__board_tokens[i][j])

        print()
        print(new_board)

    def evaluate_game(self):
        # there has to be 5 tokens on the board before there can be a win
        if self.__number_of_tokens < 5:
            return


        # check all the combinations
        for win in self.__WIN:
            cell0 = self.__board_tokens[win[0][1]][win[0][0]]
            cell1 = self.__board_tokens[win[1][1]][win[1][0]]
            cell2 = self.__board_tokens[win[2][1]][win[2][0]]

            if cell0 == cell1 == cell2:
                if cell0 != ' ':
                    self.__game_over = cell0
                    print("game over")
                    return

        if self.__number_of_tokens == 9:
            self.__game_over = 'TIE'
            print("game over - tie")
            return

    def submit_move(self, move):
        is_valid = 0

        # basic move validation
        if move[0] not in range(0, 3):
            is_valid = 0
        elif move[1] not in range(0, 3):
            is_valid = 0
        elif self.__board_tokens[move[1]][move[0]] != ' ':
            is_valid = 0
        else:
            is_valid = 1

        if is_valid == 1:
            self.__board_tokens[move[1]][move[0]] = move[2]  # token
            self.__number_of_tokens += 1
            self.show_board()
            self.evaluate_game()

        return is_valid

    def GetTokenState(self):
        return self.__board_tokens

    def GetWinningMoves(self):
        return self.__WIN