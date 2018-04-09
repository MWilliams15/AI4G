from Goal import Goal
from Action import Action
from GameState import GameState

working = True

if working:
    goal1 = Goal("Get a high distinction", 1)
    goal2 = Goal("Have fun!",5)
    goal3 = Goal("Sleep",0)
    goals = [goal1,goal2,goal3]
    game_state = GameState(goals)

    #actions
    action1 = Action("Study...",game_state,[
        {"goal":goal1,"insistance_change": -2},
        {"goal":goal2,"insistance_change": 1},
        {"goal":goal3,"insistance_change": 3},
    ])
    action2 = Action("Party!!",game_state,[
        {"goal":goal2,"insistance_change": -3},
        {"goal":goal3,"insistance_change": 3},
    ])
    action3 = Action("Go to bed",game_state,[
        {"goal":goal3,"insistance_change": -7},
    ])

    actions = [action1, action2, action3]
else:
    goal1 = Goal("Get a high distinction", 10)
    goal2 = Goal("Sleep", 3)
    goals = [goal1, goal2]
    game_state = GameState(goals)

    # actions
    action1 = Action("Study...",game_state, [
        {"goal": goal1, "insistance_change": -3},
        {"goal": goal2, "insistance_change": 1},
    ])
    action2 = Action("Go to bed",game_state, [
        {"goal": goal1, "insistance_change": 1},
        {"goal": goal2, "insistance_change": -4},
    ])

    actions = [action1, action2]


goals_fulfilled = False

while not goals_fulfilled:

    #find goal with highest insistance
    current_goal = max(goals, key=lambda item: item.GetGoalInsistance())
    print("Goal with highest insistance is:{}".format(current_goal.GetGoalName()))

    #find all the actions that will satisfy this goal
    actions_for_goal = list(filter(lambda item:item.AlleviatesGoal(current_goal),actions))

    #find action that will satisfy the best - by having the lowest resulting discontent
    if len(actions_for_goal) > 0:
        current_action = min(actions_for_goal, key=lambda item: item.GetDiscontent())
        print("Chosen action is {}".format(current_action.GetActionDescription()))

        #apply the action
        current_action.PerformAction()

    #determine if there are more goals to fulfil
    goals_fulfilled = True

    for goal in goals:
        if goal.GetGoalInsistance() > 0:
            goals_fulfilled = False

for goal in goals:
    print("Name:{},Insistance:{}".format(goal.GetGoalName(),goal.GetGoalInsistance()))