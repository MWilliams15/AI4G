from weapon import  *

class WeaponFactory(object):
   def GetWeapon(self, type):
        if type is 'ROCKET_LAUNCHER':
           return RocketLauncher()
        elif type is 'RIFLE':
            return Rifle()
        elif type is 'HAND_GRENADE':
            return HandGrenade()
        elif type is 'HAND_GUN':
            return HandGun()

