'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
import random
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

        # data for drawing this agent
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-1.0,  3),
            Point2D(-1.0,  0.0),
            Point2D(1.0,  0.0),
            Point2D(1.0,   3)
        ]

        self.health = 50



    def render(self, color=None):
        ''' Draw the triangle agent with color'''
        # draw the ship
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)


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
        self.health -= 25

        if self.health <= 0:
            cx = self.world.cx  # width
            cy = self.world.cy  # height
            margin = min(cx, cy) * (1 / 6)  # use this for padding in the next line

            minx = int(0 + margin)
            maxx = int(cx - margin)
            miny = int(0 + margin)
            maxy = int(cy - margin)

            new_x = random.randint(minx,maxx)
            new_y = random.randint(miny,maxy)

            self.pos = Vector2D(new_x,new_y)
            self.health = 50