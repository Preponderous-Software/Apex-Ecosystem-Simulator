import random
from entity.drawableEntity import DrawableEntity


# @author Daniel McCoy Stephenson
# @since September 15th, 2024
class Berries(DrawableEntity):
    def __init__(self):
        DrawableEntity.__init__(self, "Berries", (75, 0, 130), False)
        self.energy = random.randrange(10, 20)
    
    def getEnergy(self):
        return self.energy