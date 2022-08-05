import random
from chicken import Chicken
from entity import Entity
from grass import Grass
from pig import Pig
from rabbit import Rabbit


# @author Daniel McCoy Stephenson
# @since August 2nd, 2022
class Fox(Entity):
    def __init__(self, name):
        Entity.__init__(self, name, random.randrange(50, 100), True, [Chicken, Pig, Rabbit])
        self.color = (255, random.randrange(163, 167), 0)

    # Returns the color of the entity.
    def getColor(self):
        return self.color