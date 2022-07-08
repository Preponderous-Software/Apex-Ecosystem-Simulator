from entity import Entity


# @author Daniel McCoy Stephenson
# @since June 7th, 2022
class Grass(Entity):

    def __init__(self):
        Entity.__init__(self, "Grass")
        self.energy = 100