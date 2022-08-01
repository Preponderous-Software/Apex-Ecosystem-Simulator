import random
from chicken import Chicken
from cow import Cow
from entity import Entity
from pig import Pig


# @author Daniel McCoy Stephenson
# @since July 27th, 2022
class Wolf(Entity):

    def __init__(self, name):
        Entity.__init__(self, name, random.randrange(60, 70), True, [Chicken, Pig, Cow])
        self.color = (145, random.randrange(145, 155), random.randrange(145, 155))

    def getColor(self):
        return self.color