'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform, randint

from weaponfactory import WeaponFactory

GUN_MODES = {
    KEY._1: 'RIFLE',
    KEY._2: 'ROCKET_LAUNCHER',
    KEY._3: 'HAND_GUN',
    KEY._4: 'HAND_GRENADE',
}

class Shooter(object):


    def __init__(self, world=None, scale=30.0, mass=1.0, weapon='RIFLE'):
        # keep a reference to the world object
        self.world = world
        self.weapon = weapon

        self.pos = self.initial_pos()
        self.vel = Vector2D()
        self.heading = Vector2D(sin(0), cos(0))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.force = Vector2D()  # current steering force

        # data for drawing this agent
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]


    def calculate(self):
        # calculate the current steering force
        force = self.aim()
        self.force = force
        return force

    def update(self, delta):
        ''' update vehicle position and orientation '''
        # calculate and set self.force to be applied
        force = self.calculate()

        self.heading = force.get_normalised()
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