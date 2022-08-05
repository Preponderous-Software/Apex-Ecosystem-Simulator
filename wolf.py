import random
from chicken import Chicken
from cow import Cow
from entity import Entity
from fox import Fox
from pig import Pig
from rabbit import Rabbit


# @author Daniel McCoy Stephenson
# @since July 27th, 2022
class Wolf(Entity):
    def __init__(self, name):
        Entity.__init__(self, name, random.randrange(100, 200), True, [Chicken, Pig, Cow, Fox, Rabbit])
        self.color = (145, random.randrange(145, 155), random.randrange(145, 155))

    # Returns the color of the entity.
    def getColor(self):
        return self.color