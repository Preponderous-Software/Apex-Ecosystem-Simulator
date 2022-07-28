import random
from entity import Entity


# @author Daniel McCoy Stephenson
# @since July 27th, 2022
class Pig(Entity):

    def __init__(self, name):
        Entity.__init__(self, name)
        self.energy = random.randrange(50, 100)
        self.color = (255, random.randrange(170, 190), random.randrange(180, 200))
    
    def getEnergy(self):
        return self.energy

    def addEnergy(self, amount):
        self.energy += amount
    
    def removeEnergy(self, amount):
        self.energy -= amount

    def getColor(self):
        return self.color