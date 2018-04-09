class Action:
    #actions have a list of effects which contains the goal and its insistance change
    def __init__(self, description, effects,cost):
        self.effects = effects
        self.description = description
        self.cost = cost

    #def PerformAction(self):
    #    for effect in self.__effects:
    #        effect["goal"].UpdateGoalInsistance(effect["insistance_change"])
    #        self.__game_state.money += effect["cost"]

    #def GetDiscontent(self):
    #    total_discontent = 0
    #    goal_counted = False

        # for every goal
    #    for goal in self.__game_state.goals:
    #        goal_counted = False
            #do we have this goal?
            #if we do, take into account this action
    #        for effect in self.__effects:
    #            if goal == effect["goal"]:
    #                insistance = goal.GetGoalInsistance()
    #                final_insistance = insistance + effect["insistance_change"]
    #                total_discontent += final_insistance * final_insistance
    #                goal_counted = True
    #                break

    #        if not goal_counted:
     #           total_discontent += goal.GetGoalInsistance() * goal.GetGoalInsistance()

      #  return total_discontent


    #def AlleviatesGoal(self,goal):
    #    for effect in self.__effects:
    #        if effect["goal"] == goal:
    #            if effect["insistance_change"] < 0:
    #                return True
    #    return False

    #def AlleviatesGoal_Affordable(self,goal):


    #    for effect in self.__effects:
     #       if effect["goal"] == goal:
     #           if effect["insistance_change"] < 0:
     #              if effect["cost"] + self.__game_state.money >= 0:
     #                   return True


     #   return False

    #def GetActionDescription(self):
    #    return self.__description

    #def affordable(self):
        #print("funds = {}".format(self.__game_state.money))
     #   can_afford = True

     #   for effect in self.__effects:
      #      if effect["cost"] + self.__game_state.money < 0:
                #print("{} is not affordable".format(self.__description))
 #               return False
#
  #      return True
