import random
from grass import Grass
from livingEntity import LivingEntity


# @author Daniel McCoy Stephenson
# @since July 31st, 2022
class Cow(LivingEntity):
    def __init__(self, name):
        LivingEntity.__init__(self, name, (random.randrange(59, 61), random.randrange(41, 45), random.randrange(29, 33)), random.randrange(40, 50), [Grass])