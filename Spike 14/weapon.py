from bullet import Bullet

class Weapon(object):
    def __init__(self, speed, accuracy=100):
        self.speed = speed
        self.accuracy = accuracy
        self.bullet = None

    def Fire(self,world,pos):
        print("Fire weapon!")
        self.bullet = Bullet(self,world,pos)
        world.bullet = self.bullet

class RocketLauncher(Weapon):
    def __init__(self):
        Weapon.__init__(self,speed=500,accuracy=90)

class Rifle(Weapon):
    def __init__(self):
        Weapon.__init__(self,speed=2000,accuracy=90)

class HandGrenade(Weapon):
    def __init__(self):
        Weapon.__init__(self,speed=500,accuracy=25)

class HandGun(Weapon):
    def __init__(self):
        Weapon.__init__(self,speed=2000,accuracy=25)