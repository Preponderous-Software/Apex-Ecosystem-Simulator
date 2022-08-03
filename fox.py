import random
from chicken import Chicken
from cow import Cow
from entity import Entity
from grass import Grass
from pig import Pig


# @author Daniel McCoy Stephenson
# @since July 27th, 2022
class Fox(Entity):

    def __init__(self, name):
        Entity.__init__(self, name, random.randrange(50, 100), True, [Chicken, Pig])
        self.color = (255, random.randrange(163, 167), 0)

    def getColor(self):
        return self.color