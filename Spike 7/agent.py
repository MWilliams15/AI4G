'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform, randint
from path import Path

AGENT_MODES = {
    KEY._8: 'alignment',
    KEY._9: 'cohesion',
    KEY._0: 'separation',
    KEY.T: 'combined'

}

class Agent(object):

    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        ### ADD 'normal' and 'fast' speeds here
        'normal': 0.5,
        'fast': 0.1,
    }

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='combined'):
        # keep a reference to the world object
        self.world = world
        self.mode = mode
        # where am i and where am i going? random start pos
        dir = radians(random()*360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.force = Vector2D()  # current steering force
        self.accel = Vector2D() # current acceleration due to force
        self.mass = mass
        self.neighbours = []

        # data for drawing this agent
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]
        ### path to follow?
        self.path = Path()
        self.randomise_path()  # <-- Doesn’t exist yet but you’ll create it
        self.waypoint_threshold = 0.0  # <-- Work out a value for this as you test

        ### wander details
        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 3.9 * scale
        self.wander_radius = 0.2 * scale
        self.wander_jitter = 4.3 * scale
        self.bRadius = scale

        # Force and speed limiting code
        # limits
        self.max_speed = 20.0 * scale
        ## max_force
        self.max_force = 500.0

        # debug draw info?
        self.show_info = False

        #group variables
        self.wander_var = 1
        self.alignment_var = 1
        self.cohesion_var = 1

    def calculate(self,delta):
        # calculate the current steering force
        mode = self.mode
        if mode == 'alignment':
            force = self.group_alignment()
        elif mode == 'cohesion':
            force = self.group_cohesion()
        elif mode == 'separation':
            force = self.group_separation()
        elif mode == 'combined':
            force = self.combined(delta)
        else:
            force = Vector2D()
        self.force = force
        return force

    def update(self, delta):
        ''' update vehicle position and orientation '''
        self.find_neighbours()
        # calculate and set self.force to be applied
        force = self.calculate(delta)
        force.truncate(self.max_force)  # <-- new force limiting code

        # determin the new accelteration
        self.accel = force / self.mass  # not needed if mass = 1.0
        # new velocity
        self.vel += self.accel * delta
        # check for limits of new velocity
        self.vel.truncate(self.max_speed)
        # update position
        self.pos += self.vel * delta
        # update heading is non-zero velocity (moving)
        if self.vel.length_sq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()
        # treat world as continuous space - wrap new position if needed
        self.world.wrap_around(self.pos)
    def render(self, color=None):
        ''' Draw the triangle agent with color'''
        # draw the path if it exists and the mode is follow
        if self.mode == 'follow_path':
            self.path.render()

        # draw the ship
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)

        # draw wander info?
        # draw wander info?
        if self.mode == 'wander':
            # calculate the center of the wander circle in front of the agent
            wnd_pos = Vector2D(self.wander_dist, 0)
            wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
            # draw the wander circle
            egi.green_pen()
            egi.circle(wld_pos, self.wander_radius)
            # draw the wander target (little circle on the big circle)
            egi.red_pen()
            wnd_pos = (self.wander_target + Vector2D(self.wander_dist, 0))
            wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
            egi.circle(wld_pos, 3)

        # add some handy debug drawing info lines - force and velocity
        if self.show_info:
            s = 0.5 # <-- scaling factor
            # force
            egi.red_pen()
            egi.line_with_arrow(self.pos, self.pos + self.force * s, 5)
            # velocity
            egi.grey_pen()
            egi.line_with_arrow(self.pos, self.pos + self.vel * s, 5)
            # net (desired) change
            egi.white_pen()
            egi.line_with_arrow(self.pos+self.vel * s, self.pos+ (self.force+self.vel) * s, 5)
            egi.line_with_arrow(self.pos, self.pos+ (self.force+self.vel) * s, 5)

    def speed(self):
        return self.vel.length()

    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def flee(self, hunter_pos):
        ''' move away from hunter position '''
        ## add panic distance (second)
        panic_range = 100
        to_target = hunter_pos - self.pos
        dist = to_target.length()


        if dist > panic_range:
            return Vector2D()

        ## add flee calculations (first)
        desired_vel = (self.pos - hunter_pos).normalise() * self.max_speed
        return (desired_vel - self.vel)
        return Vector2D()

    def arrive(self, target_pos, speed):
        ''' this behaviour is similar to seek() but it attempts to arrive at
            the target position with a zero velocity'''
        decel_rate = self.DECELERATION_SPEEDS[speed]
        to_target = target_pos - self.pos
        dist = to_target.length()
        if dist > 0:
            # calculate the speed required to reach the target given the
            # desired deceleration rate
            speed = dist / decel_rate
            # make sure the velocity does not exceed the max
            speed = min(speed, self.max_speed)
            # from here proceed just like Seek except we don't need to
            # normalize the to_target vector because we have already gone to the
            # trouble of calculating its length for dist.
            desired_vel = to_target * (speed / dist)
            return (desired_vel - self.vel)
        return Vector2D(0, 0)

    def pursuit(self, evader):
        ''' this behaviour predicts where an agent will be in time T and seeks
            towards that point to intercept it. '''
        ## OPTIONAL EXTRA... pursuit (you'll need something to pursue!)
        return Vector2D()

    def wander(self, delta):
        ''' Random wandering using a projected jitter circle. '''

        wt = self.wander_target

        # this behaviour is dependent on the update rate, so this line must
        # be included when using time independent framerate.
        jitter_tts = self.wander_jitter * delta  # this time slice

        # first, add a small random vector to the target's position
        wt += Vector2D(uniform(-1, 1) * jitter_tts, uniform(-1, 1) * jitter_tts)

        # re-project this new vector back on to a unit circle
        wt.normalise()

        # increase the length of the vector to the same as the radius
        # of the wander circle
        wt *= self.wander_radius

        # move the target into a position WanderDist in front of the agent
        target = wt + Vector2D(self.wander_dist, 0)

        # project the target into world space
        wld_target = self.world.transform_point(target, self.pos, self.heading, self.side)

        # and steer towards it
        return self.seek(wld_target)

    def randomise_path(self):
        cx = self.world.cx  # width
        cy = self.world.cy  # height
        margin = min(cx, cy) * (1 / 6)  # use this for padding in the next line ...

        minx = 0 + margin
        maxx = cx - margin
        miny = 0 + margin
        maxy = cy - margin

        num_points = randint(3, 9)

        self.path.create_random_path(num_points,minx,miny,maxx,maxy)  # you have to figure out the parameters

    def follow_path(self):
        #if we are heading to the last point -- arrive
        if self.path.is_finished():
            return self.arrive(self.path.current_pt(), "normal")
        #go to the next waypoint
        else:
            to_target = self.path.current_pt() - self.pos
            dist = to_target.length()

            threshold = 50

            # if we are close enough to the current point, go to the next one
            if dist < threshold:
                self.path.inc_current_pt()

            #seek the current point
            return self.seek(self.path.current_pt())


    def modify_variables(self,variable,increase):
        if variable is 'alignment':
            if increase:
                self.alignment_var += 0.1
            else: self.alignment_var -= 0.1

        elif variable is 'cohesion':
            if increase:
                self.cohesion_var += 0.1
            else:
                self.cohesion_var -= 0.1

        elif variable is 'wander':
            if increase:
                self.wander_var += 0.1
            else:
                self.wander_var -= 0.1


        print("alignment: {}, cohesion: {}, wander:{}".format(self.alignment_var,self.cohesion_var,self.wander_var))

    def find_neighbours(self):
        radius = 50
        self.neighbours = []
        bots = self.world.agents

        for bot in bots:
            if self == bot:
                continue
            else:
                to = self.pos - bot.pos
                # take into account the bounding radius
                if to.length() < radius:
                    self.neighbours.append(bot)

    def group_alignment(self):
        AvgHeading = Vector2D()
        AvgCount = 0

        for bot in self.neighbours:
            AvgHeading += bot.heading
            AvgCount += 1

        if AvgCount > 0:
            AvgHeading /= float(AvgCount)
            AvgHeading -= self.heading

        return AvgHeading * self.max_speed


    def group_cohesion(self):
        CentreMass = Vector2D()
        SteeringForce = Vector2D()
        AvgCount = 0
        for bot in self.neighbours:
            CentreMass += bot.pos
            AvgCount += 1

        if AvgCount > 0:
            CentreMass /= float(AvgCount)
            SteeringForce = self.seek(CentreMass)

        return SteeringForce * self.max_speed

    def group_separation(self):
        SteeringForce = Vector2D()
        for bot in self.neighbours:
            ToBot = self.pos - bot.pos

            # scale based on inverse distance to neighbour
            SteeringForce += ToBot / ToBot.length()

        return SteeringForce * self.max_speed


    def combined(self,delta):
        force = self.wander(delta) * self.wander_var
        force += self.group_alignment() * self.alignment_var
        force += self.group_cohesion() * self.cohesion_var




        force.truncate(self.max_force)

        return force