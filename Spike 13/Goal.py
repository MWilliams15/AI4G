
class Goal:

    def __init__(self, goal_name,goal_insistance):
        self.goal_name = goal_name
        self.goal_insistance = goal_insistance

    def GetGoalInsistance(self):
        return self.goal_insistance

    def GetGoalName(self):
        return self.goal_name

    def UpdateGoalInsistance(self, insistance_change):
        self.goal_insistance += insistance_change

        if self.goal_insistance < 0:
            self.goal_insistance = 0