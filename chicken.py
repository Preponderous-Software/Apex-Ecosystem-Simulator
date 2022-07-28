import random
from entity import Entity


# @author Daniel McCoy Stephenson
# @since June 7th, 2022
class Chicken(Entity):

    def __init__(self, name):
        Entity.__init__(self, name, random.randrange(40, 60))
        self.color = (random.randrange(240, 255), random.randrange(240, 255), random.randrange(240, 255))

    def getColor(self):
        return self.color