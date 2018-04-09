class Action:
    #actions have a list of effects which contains the goal and its insistance change
    def __init__(self, description,game_state, effects, ):
        self.__effects = effects
        self.__description = description
        self.__game_state = game_state

    def PerformAction(self):
        for effect in self.__effects:
            effect["goal"].UpdateGoalInsistance(effect["insistance_change"])

    def GetDiscontent(self):
        total_discontent = 0
        goal_counted = False

        # for every goal
        for goal in self.__game_state.goals:
            goal_counted = False
            # do we have this goal?
            # if we do, take into account this action
            for effect in self.__effects:
                if goal == effect["goal"]:
                    insistance = goal.GetGoalInsistance()
                    final_insistance = insistance + effect["insistance_change"]
                    total_discontent += final_insistance * final_insistance
                    goal_counted = True
                    break

            if not goal_counted:
                total_discontent += goal.GetGoalInsistance() * goal.GetGoalInsistance()

        return total_discontent

    def AlleviatesGoal(self,goal):
        for effect in self.__effects:
            if effect["goal"] == goal:
                if effect["insistance_change"] < 0:
                    return True
        return False

    def GetActionDescription(self):
        return self.__description