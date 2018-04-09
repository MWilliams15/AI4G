#define a list of goals - the goals aimed to be reduced to 0 - satisfied
#define a list of actions - actions reduce the goal insistance

#each "tick"
    #which goal has the highest insistance?
        # how should we handle two goals with the same insistance?
        # if there all goals are satsfied we can just stop
    #choose an action will satisfy this goal appropriately

from Goal import Goal
from Action import Action
from GameState import  GameState
from copy import deepcopy


game_state = GameState()


states = [[game_state,game_state.base_action]]

best_action = None
best_value = 999999
best_plan = []
changed = True
while states:
    current_value = states[-1][0].GetCurrentStateDiscontent()
    #print(states[-1][1].GetActionDescription())
    #print(states)

    if changed:
        if len(states) == 1:
            print("-->{} ({}) ({})".format(states[-1][1].description,states[-1][0].money,states[-1][0].GetCurrentStateDiscontent()))
        elif len(states) == 2:
            print("   -->{} ({}) ({})".format(states[-1][1].description,states[-1][0].money,states[-1][0].GetCurrentStateDiscontent()))
        elif len(states) == 3:
            print("      -->{} ({}) ({})".format(states[-1][1].description,states[-1][0].money,states[-1][0].GetCurrentStateDiscontent()))


    if len(states) >= 3:
        if current_value < best_value:
            best_value = current_value
            #get the best plan
            best_plan = [state[1] for state in states if state[1]] + [best_value]
        states.pop()
        continue


    next_action = states[-1][0].next_action()
    if next_action:
        next_state = deepcopy(states[-1][0])
        states.append([next_state,None])
        states[-1][1] = next_action
        next_state.reset()
        ##############
        states[-1][0].apply_action(next_action)
        changed = True


    else:
        states.pop()


print(best_plan[0].description)
print(best_plan[1].description)
print(best_plan[2].description)
print("Final Discontent:{}".format( best_plan[3]))


