import random
from entity.grass import Grass
from entity.livingEntity import LivingEntity


# @author Daniel McCoy Stephenson
# @since July 27th, 2022
class Pig(LivingEntity):
    def __init__(self, name):
        LivingEntity.__init__(self, name, (255, random.randrange(170, 190), random.randrange(180, 200)), False, random.randrange(30, 40), [Grass])