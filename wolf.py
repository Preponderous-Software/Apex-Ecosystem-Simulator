import random
from entity import Entity


# @author Daniel McCoy Stephenson
# @since July 27th, 2022
class Wolf(Entity):

    def __init__(self, name):
        Entity.__init__(self, name, random.randrange(50, 75))
        self.color = (145, random.randrange(145, 155), random.randrange(145, 155))

    def getColor(self):
        return self.color