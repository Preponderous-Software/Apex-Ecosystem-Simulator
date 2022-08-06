from math import ceil
from operator import truediv
import random
from chicken import Chicken
from cow import Cow
from eatActionHandler import EatActionHandler
from entity import Entity
from environment import Environment
from excrement import Excrement
from excreteActionHandler import ExcreteActionHandler
from fox import Fox
from grass import Grass
from livingEntity import LivingEntity
from moveActionHandler import MoveActionHandler
from pig import Pig
from rabbit import Rabbit
from reproduceActionHandler import ReproduceActionHandler
from wolf import Wolf


# @author Daniel McCoy Stephenson
# @since July 26th, 2022
class Simulation:
    def __init__(self, name, config, gameDisplay):        
        self.config = config
        self.gameDisplay = gameDisplay

        self.environment = Environment(name, self.config.gridSize)

        self.moveActionHandler = MoveActionHandler(self.environment)
        self.eatActionHandler = EatActionHandler(self.environment)
        self.excreteActionHandler = ExcreteActionHandler(self.environment)
        self.reproduceActionHandler = ReproduceActionHandler(self.environment)

        self.initializeLocationWidthAndHeight()

        self.entities = []
        self.livingEntities = []
        self.excrement = []

        self.running = True

        self.numTicks = 0
    
    def initializeLocationWidthAndHeight(self):
        x, y = self.gameDisplay.get_size()
        self.locationWidth = x/self.environment.getGrid().getRows()
        self.locationHeight = y/self.environment.getGrid().getColumns()
    
    def addEntity(self, entity: Entity):
        self.entities.append(entity)
        if isinstance(entity, LivingEntity):
            self.livingEntities.append(entity)
        if type(entity) is Excrement:
            self.excrement.append(entity)
    
    def removeEntityFromLocation(self, entity: Entity):
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
        location = grid.getLocation(locationID)
        if location.isEntityPresent(entity):
            location.removeEntity(entity)
    
    def printDeathInfo(self, entity, oldestLivingEntity):
            toPrint = entity.getName() + " has died."
            if len(self.livingEntities) > 0:
                if entity.getID() == oldestLivingEntity.getID():
                    toPrint += " They were the oldest living entity."
            print(toPrint)

    def removeEntity(self, entity: Entity):
        if len(self.livingEntities) > 0:
            oldestLivingEntity = self.livingEntities[0]

        self.entities.remove(entity)
        self.removeEntityFromLocation(entity)
        if isinstance(entity, LivingEntity):
            self.livingEntities.remove(entity)
            self.printDeathInfo(entity, oldestLivingEntity)
        if type(entity) is Excrement:
            self.excrement.remove(entity)
        
    def initializeEntities(self):
        for i in range(self.config.numGrassEntities):
            self.addEntity(Grass())

        for i in range(self.config.numChickensToStart):
            self.addEntity(Chicken("Chicken"))

        for i in range(self.config.numPigsToStart):
            self.addEntity(Pig("Pig"))

        for i in range(self.config.numWolvesToStart):
            self.addEntity(Wolf("Wolf"))
        
        for i in range (self.config.numCowsToStart):
            self.addEntity(Cow("Cow"))
        
        for i in range(self.config.numFoxesToStart):
            self.addEntity(Fox("Fox"))

        for i in range(self.config.numRabbitsToStart):
            self.addEntity(Rabbit("Rabbit"))

    def placeEntities(self):
        for entity in self.entities:
            self.environment.addEntity(entity)
    
    def getNumberOfEntitiesOfType(self, entityType):
        count = 0
        for entity in self.entities:
            if type(entity) is entityType:
                count += 1
        return count

    def getNumberOfLivingEntitiesOfType(self, entityType):
        count = 0
        for entity in self.livingEntities:
            if type(entity) is entityType:
                count += 1
        return count
    
    def getNumLivingEntities(self):
        return len(self.livingEntities)
    
    def getNumExcrement(self):
        return len(self.excrement)

    def performExcrementCheck(self, excrement):
            if (self.numTicks - excrement.getTick()) > self.config.grassGrowTime:
                locationID = excrement.getLocationID()
                grid = self.environment.getGrid()
                location = grid.getLocation(locationID)
                
                self.removeEntity(excrement)
                grass = Grass()
                location.addEntity(grass)
                self.addEntity(grass)

    def growGrass(self):
        for excrement in self.excrement:
            self.performExcrementCheck(excrement)
            
    def initiateEntityActions(self):
        for entity in self.livingEntities:
            self.moveActionHandler.initiateMoveAction(entity)
            if entity.needsEnergy():
                self.eatActionHandler.initiateEatAction(entity, self.removeEntity)
            else:
                if random.randrange(0, 100) < (self.config.chanceToExcrete*100):
                    self.excreteActionHandler.initiateExcreteAction(entity, self.addEntity, self.numTicks)
                if random.randrange(0, 100) < (self.config.chanceToReproduce*100):
                    self.reproduceActionHandler.initiateReproduceAction(entity, self.addEntity)

    def decreaseEnergyForLivingEntities(self):
        for entity in self.livingEntities:
            entity.removeEnergy(1)
            if entity.getEnergy() <= 0:
                self.removeEntity(entity)
    
    def cleanup(self):
        print("---")
        print("State of environment:")
        self.environment.printInfo()
        print("Length of simulation:", self.numTicks, "ticks")
        print("---")
    
    def update(self):
            # initiate entity actions
            self.initiateEntityActions()
            
            # decrease energy for living entities
            self.decreaseEnergyForLivingEntities()
            
            # make grass grow
            self.growGrass()