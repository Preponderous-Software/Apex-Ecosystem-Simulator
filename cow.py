import random
from entity import Entity
from grass import Grass


# @author Daniel McCoy Stephenson
# @since July 31st, 2022
class Cow(Entity):
    def __init__(self, name):
        Entity.__init__(self, name, random.randrange(40, 50), True, [Grass])
        self.color = (random.randrange(59, 61), random.randrange(41, 45), random.randrange(29, 33))

    # Returns the color of the entity.
    def getColor(self):
        return self.color