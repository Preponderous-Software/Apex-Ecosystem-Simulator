from entity import Entity


# @author Daniel McCoy Stephenson
# @since June 7th, 2022
class Chicken(Entity):

    def __init__(self, name):
        Entity.__init__(self, name)
        self.energy = 100