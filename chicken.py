import random
from entity import Entity
from grass import Grass


# @author Daniel McCoy Stephenson
# @since July 7th, 2022
class Chicken(Entity):

    def __init__(self, name):
        Entity.__init__(self, name, random.randrange(20, 30), True, [Grass])
        self.color = (random.randrange(245, 249), random.randrange(245, 249), random.randrange(245, 249))

    def getColor(self):
        return self.color