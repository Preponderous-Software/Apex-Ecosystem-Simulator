import random
from entity.drawableEntity import DrawableEntity


# @author Daniel McCoy Stephenson
# @since July 7th, 2022
class BerryBush(DrawableEntity):
    def __init__(self):
        DrawableEntity.__init__(self, "BerryBush", (34, 139, 34), False)
        self.energy = random.randrange(10, 20)
        self.tick = 1
    
    def getEnergy(self):
        return self.energy
    
    def getTick(self):
        return self.tick

    def incrementTick(self):
        self.tick += 1