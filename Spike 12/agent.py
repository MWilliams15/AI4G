'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from graphics import egi, KEY
from path import Path


class Agent(object):


    def __init__(self):
        self.pos = Vector2D(10, 10)

        # data for drawing this agent
        self.color = 'GREEN'

        ### path to follow?
        self.path = Path()


    def update(self):
        self.follow_path()

    def render(self, color=None):

        # draw the ship
        egi.set_pen_color(name=self.color)

        egi.cross(self.pos,10)
        egi.circle(self.pos,10)



    def follow_path(self):
        to_target = self.path.current_pt() - self.pos
        dist = to_target.length()

        threshold = 5

        # if we are close enough to the current point, go to the next one
        if dist < threshold and not self.path.is_finished():
            self.path.inc_current_pt()

        if self.pos.x > self.path.current_pt().x:
            self.pos.x -= 5
        if self.pos.x < self.path.current_pt().x:
            self.pos.x += 5
        if self.pos.y > self.path.current_pt().y:
            self.pos.y -= 5
        if self.pos.y < self.path.current_pt().y:
            self.pos.y += 5


