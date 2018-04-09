'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D,PointToVector2D,Vector2DToPoint
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform, randint
from point2d import  Point2D


class Bullet(object):

    def __init__(self,weapon, world=None, pos = Vector2D()):
        # keep a reference to the world object
        self.world = world
        self.weapon = weapon
        # where am i and where am i going? random start pos
        self.pos = pos + Vector2D(5,0)
        self.vel = Vector2D()

        # Force and speed limiting code
        # limits
        self.speed = self.weapon.speed
        self.radius = 3

        # debug draw info?
        self.show_info = True

        self.vel = self.target(self.world.target)

    def update(self, delta):

        # update position
        self.pos += self.vel * delta

        self.check_for_collision()

        #destroy if out of bounds
        if self.pos.x >= self.world.cx:
            self.world.bullet = None
        if self.pos.x <= 0:
            self.world.bullet = None

        if self.pos.y >= self.world.cy:
            self.world.bullet = None
        if self.pos.y <= 0:
            self.world.bullet = None

    def render(self, color=None):

        egi.circle(self.pos,self.radius)

    def speed(self):
        return self.vel.length()


    def target(self, target):
        ''' move towards target position '''
        target_offset = self.pos - target.pos

        target_distance = PointToVector2D(target_offset).length()



        target_direction = PointToVector2D(target_offset).normalise()

        relative_velocity = target_direction * self.speed

        relative_speed = relative_velocity.dot(target_direction)

        if (relative_speed <= 0.0):
            intercept_time = 1.0
        else:
            intercept_time = target_distance / relative_speed

        intercept_location = target.pos + target.vel * intercept_time

        intercept_point = intercept_location - self.pos
        if self.miss():
            print("miss")
            intercept_point += Point2D(100,100)

        aim = PointToVector2D(intercept_point).normalise()
        vel = aim * self.speed

        return vel

    def check_for_collision(self):
        rightmost_point = Point2D(self.pos.x + self.radius,self.pos.y)
        leftmost_point = Point2D(self.pos.x - self.radius,self.pos.y)
        hit = False


        if self.world.target.point_inside(rightmost_point):
            hit = True
        elif self.world.target.point_inside(leftmost_point):
            hit = True

        if hit:
            self.world.bullet = None
            self.world.target.hit()


    def miss(self):
        chance = randint(1,100)

        if chance > self.weapon.accuracy:
            return True
        else:
            return False

