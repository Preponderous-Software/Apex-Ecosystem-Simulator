import random
from grass import Grass
from livingEntity import LivingEntity


# @author Daniel McCoy Stephenson
# @since July 7th, 2022
class Chicken(LivingEntity):
    def __init__(self, name):
        LivingEntity.__init__(self, name, (random.randrange(245, 249), random.randrange(245, 249), random.randrange(245, 249)), random.randrange(20, 30), [Grass])