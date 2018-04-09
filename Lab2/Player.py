class Player:

    def __init__(self, name, token):
        self._token = token
        self._name = name
        self._win_count = 0

    def get_move(self):
        pass

    def get_name(self):
        return self._name

    def Winner(self):
        self._win_count += 1

    def GetWinCount(self):
        return self._win_count