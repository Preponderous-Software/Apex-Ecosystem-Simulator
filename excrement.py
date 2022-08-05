import random
from entity import Entity


# @author Daniel McCoy Stephenson
# @since July 27th, 2022
class Excrement(Entity):
    def __init__(self, tick):
        Entity.__init__(self, "Excrement", random.randrange(1, 5), False, [])
        self.color = ((random.randrange(135, 145), random.randrange(65, 75), random.randrange(15, 25)))
        self.tick = tick
    
    # Returns the color of the entity.
    def getColor(self):
        return self.color
    
    # Returns the tick at which this entity was created.
    def getTick(self):
        return self.tick