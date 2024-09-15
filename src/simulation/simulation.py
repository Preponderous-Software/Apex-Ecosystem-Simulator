import random
import pygame
from actionhandler.eatActionHandler import EatActionHandler
from actionhandler.excreteActionHandler import ExcreteActionHandler
from actionhandler.moveActionHandler import MoveActionHandler
from actionhandler.reproduceActionHandler import ReproduceActionHandler
from entity.berries import Berries
from entity.berryBush import BerryBush
from service.soundService import SoundService

from lib.pyenvlib.entity import Entity
from lib.pyenvlib.environment import Environment

from entity.chicken import Chicken
from entity.cow import Cow
from entity.excrement import Excrement
from entity.fox import Fox
from entity.grass import Grass
from entity.livingEntity import LivingEntity
from entity.pig import Pig
from entity.rabbit import Rabbit
from entity.wolf import Wolf
from entity.water import Water
from entity.rock import Rock


# @author Daniel McCoy Stephenson
# @since July 26th, 2022
class Simulation:
    def __init__(self, name, config, gameDisplay):
        self.name = name       
        self.config = config
        self.gameDisplay = gameDisplay

        self.environment = Environment(name, self.config.gridSize)

        self.soundService = SoundService()

        self.moveActionHandler = MoveActionHandler(self.environment)
        self.eatActionHandler = EatActionHandler(self.environment)
        self.excreteActionHandler = ExcreteActionHandler(self.environment)
        self.reproduceActionHandler = ReproduceActionHandler(self.environment, self.soundService, config)

        self.initializeLocationWidthAndHeight()

        self.entities = dict()
        self.livingEntityIds = []
        self.excrementIds = []
        self.berryBushIds = []

        self.running = True

        self.numTicks = 0
    
    def initializeLocationWidthAndHeight(self):
        x, y = self.gameDisplay.get_size()
        self.locationWidth = x/self.environment.getGrid().getRows()
        self.locationHeight = y/self.environment.getGrid().getColumns()
    
    def addEntity(self, entity: Entity):
        self.entities[entity.getID()] = entity
        if isinstance(entity, LivingEntity):
            self.livingEntityIds.append(entity.getID())
        if type(entity) is Excrement:
            self.excrementIds.append(entity.getID())
        if type(entity) is BerryBush:
            self.berryBushIds.append(entity.getID())
    
    def removeEntityFromLocation(self, entity: Entity):
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
        location = grid.getLocation(locationID)
        if location.isEntityPresent(entity):
            location.removeEntity(entity)
    
    def printDeathInfo(self, entity, oldestLivingEntity):
            toPrint = entity.getName() + " has died."
            if len(self.livingEntityIds) > 0:
                if entity.getID() == oldestLivingEntity.getID():
                    toPrint += " They were the oldest living entity."
            print(toPrint)

    def removeEntity(self, entity: Entity):
        if len(self.livingEntityIds) > 0:
            oldestLivingEntityId = self.livingEntityIds[0]
            oldestLivingEntity = self.entities[oldestLivingEntityId]

        del self.entities[entity.getID()]
        self.removeEntityFromLocation(entity)
        if isinstance(entity, LivingEntity):
            self.livingEntityIds.remove(entity.getID())
            self.printDeathInfo(entity, oldestLivingEntity)
            if not self.config.muted:
                self.soundService.playDeathSoundEffect()
        if type(entity) is Excrement:
            self.excrementIds.remove(entity.getID())
        if type(entity) is BerryBush:
            self.berryBushIds.remove(entity.getID())
        
    def generateMap(self):        
        for i in range(self.config.numWaterEntities):
            self.addEntity(Water())
        
        for i in range(self.config.numRockEntities):
            self.addEntity(Rock())
            
        for i in range(self.config.numGrassEntities):
            self.addEntity(Grass())
            
        for i in range(self.config.numBerriesEntities):
            self.addEntity(Berries())
            
        for i in range(self.config.numBerryBushEntities):
            self.addEntity(BerryBush())

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
        for entityId in self.entities:
            entity = self.entities[entityId]
            self.environment.addEntity(entity)
    
    def getNumberOfEntitiesOfType(self, entityType):
        count = 0
        for entityId in self.entities:
            entity = self.entities[entityId]
            if type(entity) is entityType:
                count += 1
        return count

    def getNumberOfLivingEntitiesOfType(self, entityType):
        count = 0
        for entityId in self.livingEntityIds:
            entity = self.entities[entityId]
            if type(entity) is entityType:
                count += 1
        return count
    
    def getNumLivingEntities(self):
        return len(self.livingEntityIds)
    
    def getNumExcrement(self):
        return len(self.excrementIds)

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
        for excrementId in self.excrementIds:
            excrement = self.entities[excrementId]
            self.performExcrementCheck(excrement)
    
    def growBerries(self):
        for berryBushId in self.berryBushIds:
            berryBush = self.entities[berryBushId]
            berryBush.incrementTick()
            self.performBerryBushCheck(berryBush)
    
    def performBerryBushCheck(self, berryBush):
        if (berryBush.getTick() % self.config.berryBushGrowTime) == 0 and berryBush.getEnergy() > 10:
            locationID = berryBush.getLocationID()
            grid = self.environment.getGrid()
            location = grid.getLocation(locationID)
            
            # if location does not have more than 10 berries, add a berry
            numBerries = 0
            for entity in location.getEntities():
                if type(entity) is Berries:
                    numBerries += 1
            if numBerries < 10:
                berries = Berries()
                location.addEntity(berries)
                self.addEntity(berries)
                berryBush.energy -= 1
            
    def initiateEntityActions(self):
        for entityId in self.livingEntityIds:
            entity = self.entities[entityId]
            self.moveActionHandler.initiateMoveAction(entity)
            if entity.needsEnergy():
                self.eatActionHandler.initiateEatAction(entity, self.removeEntity)
            else:
                if random.randrange(0, 100) < (self.config.chanceToExcrete*100):
                    self.excreteActionHandler.initiateExcreteAction(entity, self.addEntity, self.numTicks)
                if random.randrange(0, 100) < (self.config.chanceToReproduce*100):
                    self.reproduceActionHandler.initiateReproduceAction(entity, self.addEntity)

    def decreaseEnergyForLivingEntities(self):
        for entityId in self.livingEntityIds:
            entity = self.entities[entityId]
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

        # make berries grow
        self.growBerries()
        
        # 10% chance for berry bushes to gain energy
        for berryBushId in self.berryBushIds:
            berryBush = self.entities[berryBushId]
            if random.randrange(0, 100) < 10:
                berryBush.energy += 1