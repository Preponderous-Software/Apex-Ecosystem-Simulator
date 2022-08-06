import random
from chicken import Chicken
from livingEntity import LivingEntity
from pig import Pig
from rabbit import Rabbit


# @author Daniel McCoy Stephenson
# @since August 2nd, 2022
class Fox(LivingEntity):
    def __init__(self, name):
        LivingEntity.__init__(self,name,(255, random.randrange(163, 167), 0), random.randrange(50, 100),[Chicken, Pig, Rabbit])