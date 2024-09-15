import random
from entity.drawableEntity import DrawableEntity



# @author Daniel McCoy Stephenson
# @since August 5th, 2022
class LivingEntity(DrawableEntity):
    MALE = 0
    FEMALE = 1
    
    def __init__(self, name, color, solid, energy, edibleEntityTypes):
        DrawableEntity.__init__(self, name, color, solid)
        self.energy = energy
        self.edibleEntityTypes = edibleEntityTypes
        self.targetEnergy = energy
        self.sex = random.choice([LivingEntity.MALE, LivingEntity.FEMALE])
    
    def getEnergy(self):
        return self.energy

    def addEnergy(self, amount):
        self.energy += amount
    
    def removeEnergy(self, amount):
        self.energy -= amount

    def needsEnergy(self):
        return self.energy < self.targetEnergy

    def canEat(self, entity):
        for entityType in self.edibleEntityTypes:
            if type(entity) is entityType:
                return True
        return False

    def getSex(self):
        return self.sex