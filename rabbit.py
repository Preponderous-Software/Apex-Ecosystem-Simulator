import random
from entity import Entity
from grass import Grass


# @author Daniel McCoy Stephenson
# @since August 2nd, 2022
class Rabbit(Entity):
    def __init__(self, name):
        Entity.__init__(self, name, random.randrange(20, 30), True, [Grass])
        self.color = (250,220,200)

    # Returns the color of the entity.
    def getColor(self):
        return self.color