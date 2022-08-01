import random
from entity import Entity
from grass import Grass


# @author Daniel McCoy Stephenson
# @since June 7th, 2022
class Chicken(Entity):

    def __init__(self, name):
        Entity.__init__(self, name, random.randrange(20, 30), True, [Grass])
        self.color = (random.randrange(240, 255), random.randrange(240, 255), random.randrange(240, 255))

    def getColor(self):
        return self.color