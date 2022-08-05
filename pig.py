import random
from chicken import Chicken
from entity import Entity
from grass import Grass


# @author Daniel McCoy Stephenson
# @since July 27th, 2022
class Pig(Entity):
    def __init__(self, name):
        Entity.__init__(self, name, random.randrange(30, 40), True, [Grass])
        self.color = (255, random.randrange(170, 190), random.randrange(180, 200))

    # Returns the color of the entity.
    def getColor(self):
        return self.color