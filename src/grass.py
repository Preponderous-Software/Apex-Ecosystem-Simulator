import random
from drawableEntity import DrawableEntity


# @author Daniel McCoy Stephenson
# @since July 7th, 2022
class Grass(DrawableEntity):
    def __init__(self):
        DrawableEntity.__init__(self, "Grass", ((0, random.randrange(130, 170), 0)))
        self.energy = random.randrange(10, 20)
    
    def getEnergy(self):
        return self.energy