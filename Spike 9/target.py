'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
import time

class Target(object):


    def __init__(self, world=None, scale=30.0, mass=1.0, mode='none'):
        # keep a reference to the world object
        self.world = world
        self.mode = mode
        # where am i and where am i going? random start pos
        dir = radians(0)
        self.pos = self.initial_pos()
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.force = Vector2D()  # current steering force
        self.accel = Vector2D() # current acceleration due to force
        self.mass = mass

        # data for drawing this agent
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-1.0,  3),
            Point2D(-1.0,  0.0),
            Point2D(1.0,  0.0),
            Point2D(1.0,   3)
        ]

        # Force and speed limiting code
        # limits
        self.max_speed = 20.0 * scale
        ## max_force
        self.max_force = 500.0

        # debug draw info?
        self.show_info = True

        self.target_pos = self.pos

    def calculate(self,delta):

        return self.oscillate()

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


    def speed(self):
        return self.vel.length()

    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)


    def oscillate(self):

        threshold = 5
        cx = self.world.cx  # width
        cy = self.world.cy  # height
        margin = min(cx, cy) * (1 / 6)  # use this for padding in the next line ...

        miny = 0 + margin
        maxy = cy - margin

        xpos = cx - margin

        if self.pos.y <= miny + threshold:
            self.target_pos = Vector2D(xpos,maxy)
        elif self.pos.y >= maxy - threshold: self.target_pos = Vector2D(xpos,miny)

        return self.seek(self.target_pos)


    def initial_pos(self):
        cx = self.world.cx  # width
        cy = self.world.cy  # height
        margin = min(cx, cy) * (1 / 6)  # use this for padding in the next line ...

        maxx = cx - margin
        miny = 0 + margin

        return Vector2D(maxx,miny)

    def get_world_points(self):
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)

        return pts

    def point_inside(self,point):
        pts = self.get_world_points()

        minx = min(pts, key=lambda item: item.x).x
        maxx = max(pts, key=lambda item: item.x).x

        miny = min(pts, key=lambda item: item.y).y
        maxy = max(pts, key=lambda item: item.y).y

        if point.x < minx or point.x > maxx:
            return False
        if point.y < miny or point.y > maxy:
            return False

        return True

    def hit(self):
       time.sleep(0.5)