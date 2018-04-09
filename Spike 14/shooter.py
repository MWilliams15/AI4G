'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from vector2d import Point2D,PointToVector2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform, randint
from path import Path

from weaponfactory import WeaponFactory

GUN_MODES = {
    KEY._1: 'RIFLE',
    KEY._2: 'ROCKET_LAUNCHER',
    KEY._3: 'HAND_GUN',
    KEY._4: 'HAND_GRENADE',
}

class Shooter(object):

    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        ### ADD 'normal' and 'fast' speeds here
        'normal': 0.5,
        'fast': 0.1,
    }

    def __init__(self, world=None, scale=30.0, mass=1.0, weapon='RIFLE'):
        # keep a reference to the world object
        self.world = world
        self.weapon = weapon
        self.mode = "FOLLOW_PATH"

        self.pos = self.initial_pos()
        self.vel = Vector2D()
        self.heading = Vector2D(sin(0), cos(0))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.force = Vector2D()  # current steering force

        self.max_speed = 100
        self.max_force = 500.0

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


    def calculate(self):
        # calculate the current steering force
        force = self.follow_path()
        self.force = force
        return force

    def update(self, delta):
        ''' update vehicle position and orientation '''
        # calculate and set self.force to be applied
        if self.mode == "STOP":
            self.vel = Vector2D()
        else:
            force = self.calculate()

            # calculate and set self.force to be applied
            #force = self.calculate(delta)
            force.truncate(self.max_force)  # <-- new force limiting code

            # determin the new accelteration
            self.accel = force
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

        if self.mode == 'FOLLOW_PATH':
            self.path.render()

        # draw the ship
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)


    #--------------------------------------------------------------------------

    def aim(self):
        ''' move towards target position '''
        target = self.world.target

        if target:
            desired_vel = (target.pos - self.pos).normalise()
            return (desired_vel - self.vel)

        return Point2D()

    def initial_pos(self):
        cx = self.world.cx  # width
        cy = self.world.cy  # height

        margin = min(cx, cy) * (1 / 6)  # use this for padding in the next line ...

        xpos = cx + margin
        ypos = cy / 2

        return Vector2D(xpos, ypos)

    def fire_weapon(self):
        weapon = WeaponFactory().GetWeapon(self.weapon)
        weapon.Fire(self.world,self.pos)

    #### MOVEMENT #####

    def seek(self, target_pos):


        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

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

    def randomise_path(self):
        cx = self.world.cx  # width
        cy = self.world.cy  # height
        margin = min(cx, cy) * (1 / 6)  # use this for padding in the next line ...

        minx = 0 + margin
        maxx = cx - margin
        miny = 0 + margin
        maxy = cy - margin

        num_points = randint(3, 9)

        self.path.create_random_path(num_points, minx, miny, maxx, maxy)  # you have to figure out the parameters

    def follow_path(self):
        # if we are heading to the last point -- arrive
        if self.path.is_finished():
            vel = self.arrive(self.path.current_pt(), "normal")
            #self.randomise_path()
            return vel
        # go to the next waypoint
        else:
            to_target = self.path.current_pt() - self.pos
            dist = to_target.length()

            threshold = 50

            # if we are close enough to the current point, go to the next one
            if dist < threshold:
                self.path.inc_current_pt()

            # seek the current point
            return self.seek(self.path.current_pt())

    def dist_from_target(self):
        return PointToVector2D(self.world.target.pos - self.pos).length()