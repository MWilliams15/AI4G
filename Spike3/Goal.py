
class Goal:

    def __init__(self, goal_name,goal_insistance):
        self.__goal_name = goal_name
        self.__goal_insistance = goal_insistance

    def GetGoalInsistance(self):
        return self.__goal_insistance

    def GetGoalName(self):
        return self.__goal_name

    def UpdateGoalInsistance(self, insistance_change):
        self.__goal_insistance += insistance_change

        if self.__goal_insistance < 0:
            self.__goal_insistance = 0