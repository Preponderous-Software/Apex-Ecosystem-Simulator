import random
from entity import Entity


# @author Daniel McCoy Stephenson
# @since June 7th, 2022
class Grass(Entity):

    def __init__(self):
        Entity.__init__(self, "Grass", random.randrange(10, 20))
        self.color = ((0, random.randrange(130, 170), 0))
    
    def getColor(self):
        return self.color