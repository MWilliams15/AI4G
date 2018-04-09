class StateMachineAgent(object):
    #Attack
    #Patrol
    STATES = {"ATTACK":0,
              "PATROL":1}

    def __init__(self,shooter):
        self.current_state = self.STATES["PATROL"]
        self.shooter = shooter
        self.sm_attack = StateMachine_Attacking(shooter)
        self.sm_patrol = StateMachine_Patrol(shooter)
        self.shoot_threshold = 200

    def change_state(self):
        if self.shooter.dist_from_target() < self.shoot_threshold:
            self.current_state = self.STATES["ATTACK"]
        else:
            self.current_state = self.STATES["PATROL"]

        self.apply_state()

    def apply_state(self):
        if self.current_state == self.STATES["PATROL"]:
            self.sm_attack.wait = True
            self.sm_patrol.stop = False
        elif self.current_state == self.STATES["ATTACK"]:
            self.sm_attack.wait = False
            self.sm_patrol.stop = True

        self.sm_patrol.change_state()
        self.sm_attack.change_state()


class StateMachine_Attacking(object):
    #shoot
    #reload
    STATES = {"SHOOT": 0,
              "RELOAD": 1,
              "WAIT":2}

    def __init__(self,shooter):
        self.shooter = shooter
        self.wait = True
        self.current_state = self.STATES["WAIT"]


    def change_state(self):

        if self.wait:
            self.current_state = self.STATES["WAIT"]
        elif self.current_state == self.STATES["SHOOT"]:
                self.current_state = self.STATES["RELOAD"]
        elif self.current_state == self.STATES["RELOAD"]:
            if not self.shooter.world.bullet:
                self.current_state = self.STATES["SHOOT"]
        elif self.current_state == self.STATES["WAIT"]:
            self.current_state = self.STATES["SHOOT"]

        self.apply_state()

    def apply_state(self):
        if self.current_state == self.STATES["WAIT"]:
            pass
        elif self.current_state == self.STATES["SHOOT"]:
            self.shooter.fire_weapon()
        elif self.current_state == self.STATES["RELOAD"]:
            pass

class StateMachine_Patrol(object):
    #follow path
    #if path finished randomise path
    STATES = {"FOLLOW_PATH": 0,
              "RANDOMISE_PATH": 1,
              "STOP":2}

    def __init__(self,shooter):
        self.shooter = shooter
        self.stop = True
        self.current_state = self.STATES["STOP"]


    def change_state(self):
        if self.stop:
            self.current_state = self.STATES["STOP"]
        elif self.current_state == self.STATES["FOLLOW_PATH"]:
            if self.shooter.path.is_finished():
                self.current_state = self.STATES["RANDOMISE_PATH"]
        elif self.current_state == self.STATES["RANDOMISE_PATH"]:
            self.current_state = self.STATES["FOLLOW_PATH"]
        elif self.current_state == self.STATES["STOP"]:
            self.current_state = self.STATES["FOLLOW_PATH"]

        self.apply_state()

    def apply_state(self):
        if self.current_state == self.STATES["STOP"]:
            self.shooter.mode = "STOP"
        elif self.current_state == self.STATES["FOLLOW_PATH"]:
            self.shooter.mode = "FOLLOW_PATH"
        elif self.current_state == self.STATES["RANDOMISE_PATH"]:
            self.shooter.randomise_path()