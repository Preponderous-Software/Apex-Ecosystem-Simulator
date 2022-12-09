import random

from lib.pyenvlib.entity import Entity

from entity.drawableEntity import DrawableEntity


# @author Daniel McCoy Stephenson
# @since July 27th, 2022
class Excrement(DrawableEntity):
    def __init__(self, tick):
        DrawableEntity.__init__(self, "Excrement", ((random.randrange(135, 145), random.randrange(65, 75), random.randrange(15, 25))))
        self.tick = tick
    
    # Returns the tick at which this entity was created.
    def getTick(self):
        return self.tick