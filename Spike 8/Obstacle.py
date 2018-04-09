from graphics import egi

class Obstacle(object):
    def __init__(self,pos,radius):
        self.radius = radius
        self.pos = pos

    def render(self):
        egi.green_pen()
        egi.circle(self.pos,self.radius)