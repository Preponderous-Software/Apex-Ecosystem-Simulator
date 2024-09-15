import random

from entity.livingEntity import LivingEntity

from entity.chicken import Chicken
from entity.pig import Pig
from entity.rabbit import Rabbit


# @author Daniel McCoy Stephenson
# @since August 2nd, 2022
class Fox(LivingEntity):
    def __init__(self, name):
        LivingEntity.__init__(self,name,(255, random.randrange(163, 167), 0), False, random.randrange(50, 100),[Chicken, Pig, Rabbit])