'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from vector2d import Point2D,PointToVector2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform, randint
from path import Path

AGENT_MODES = {
    KEY._1: 'seek',
    KEY._2: 'arrive_slow',
    KEY._3: 'arrive_normal',
    KEY._4: 'arrive_fast',
    KEY._5: 'flee',
    KEY._6: 'follow_path',
    KEY._7: 'wander',
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

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='seek'):
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
        self.hiding_spot = None

        # data for drawing this agent
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]


        # Force and speed limiting code
        # limits
        self.max_speed = 20.0 * scale
        ## max_force
        self.max_force = 500.0

        # debug draw info?
        self.show_info = False

    def calculate(self,delta):
        # calculate the current steering force

        self.force = self.hide()
        return self.force

    def update(self, delta):
        ''' update vehicle position and orientation '''
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
        # draw the ship
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)

        if self.hiding_spot:
            egi.cross(self.hiding_spot,5)
        # draw wander info?

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

    def flee(self, hunter_pos):
        ''' move away from hunter position '''
        ## add panic distance (second)
        #panic_range = 90
        to_target = hunter_pos - self.pos
        dist = to_target.length()


        ##if dist > panic_range:
        #    return Vector2D()

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

    def GetHidingPosition(self, hunter, obj):
        # set the distance between the object and the hiding point
        DistFromBoundary = 30.0  # system setting
        DistAway = obj.radius + DistFromBoundary

        # get the normal vector from the hunter to the hiding point
        #use the perpendicular vector for better behaviour
        ToObj = PointToVector2D(obj.pos - hunter.pos).normalise().perp()
        # scale size past the object to the hiding location
        return (ToObj * DistAway) + obj.pos


    def hide(self):
        DistToClosest = None
        BestHidingSpot = None

        self.hiding_spot = None
        hunter = self.world.hunters[0] #only one at the moment

        # check for possible hiding spots
        hunterDist = (hunter.pos - self.pos).length()

        # too close - run away
        if hunterDist < 100:
            return self.flee(hunter.pos)

        # find somewhere to hide
        else:

            #find the closest object
            for obj in self.world.obstacles:
                HidingSpot = self.GetHidingPosition(hunter, obj)
                HidingDist = (HidingSpot - self.pos).length()

                if not DistToClosest or HidingDist < DistToClosest:
                    DistToClosest = HidingDist
                    BestHidingSpot = HidingSpot

            self.hiding_spot = BestHidingSpot

            #go there
            return self.arrive(BestHidingSpot,'fast')


