import random

#Create a class that will serve for our state machine
class StateMachine:
    __number_of_treats = 10
    __current_state = 2

    #States
    __STATE_GO_HOME = 1
    __STATE_WALK_THE_DOG = 2
    __STATE_DOG_PERFORM_TRICK = 3
    __STATE_GIVE_DOG_TREAT = 4


    #State switching logic
    def __next_state(self):
        if self.__current_state == self.__STATE_GO_HOME:
            print("Going home now...")

        elif self.__current_state == self.__STATE_WALK_THE_DOG:
            print("Walk, walk, walk...", self.__number_of_treats," treat(s) left")

            if self.__number_of_treats > 0:
                self.__current_state = self.__STATE_DOG_PERFORM_TRICK
            else:
                self.__current_state = self.__STATE_GO_HOME

        elif self.__current_state == self.__STATE_DOG_PERFORM_TRICK:
            #determine which trick we should ask
            rand = random.randint(1,3)

            if rand == 1:
                print("Sit!")
            elif rand == 2:
                print("Stay!")
            elif rand == 3:
                print("Speak!")

            #do a dice roll to find out if the trick was successful
            rand = random.randint(1,6)

            if rand == 6: #success
                self.__current_state = self.__STATE_GIVE_DOG_TREAT
                self.__number_of_treats -= 1
            else: #failed
                self.__current_state = self.__STATE_WALK_THE_DOG

        elif self.__current_state == self.__STATE_GIVE_DOG_TREAT:
            print("Good boy, have a treat!")
            self.__current_state = self.__STATE_WALK_THE_DOG

    #Run the state machine
    def run(self):
        while self.__current_state != self.__STATE_GO_HOME:
            self.__next_state()

sm = StateMachine();
sm.run();
