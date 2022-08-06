import random
from chicken import Chicken
from cow import Cow
from fox import Fox
from livingEntity import LivingEntity
from pig import Pig
from rabbit import Rabbit


# @author Daniel McCoy Stephenson
# @since July 27th, 2022
class Wolf(LivingEntity):
    def __init__(self, name):
        LivingEntity.__init__(self, name, (145, random.randrange(145, 155), random.randrange(145, 155)), random.randrange(100, 200), [Chicken, Pig, Cow, Fox, Rabbit])