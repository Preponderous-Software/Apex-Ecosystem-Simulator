import random
from entity import Entity


# @author Daniel McCoy Stephenson
# @since June 7th, 2022
class Grass(Entity):

    def __init__(self):
        Entity.__init__(self, "Grass")
        self.energy = random.randrange(1, 5)
        self.color = ((0, random.randrange(130, 170), 0))
    
    def getEnergy(self):
        return self.energy
    
    def getColor(self):
        return self.color