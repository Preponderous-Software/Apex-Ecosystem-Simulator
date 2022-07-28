import random
from entity import Entity


# @author Daniel McCoy Stephenson
# @since June 27th, 2022
class Excrement(Entity):

    def __init__(self, tick):
        Entity.__init__(self, "Excrement", random.randrange(5, 15))
        self.color = ((random.randrange(135, 145), random.randrange(65, 75), random.randrange(15, 25)))
        self.tick = tick
    
    def getColor(self):
        return self.color
    
    def getTick(self):
        return self.tick