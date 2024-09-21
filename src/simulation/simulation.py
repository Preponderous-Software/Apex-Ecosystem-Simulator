import random
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
    # constructors ------------------------------------------------------------
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
    
    # public methods ---------------------------------------------------------
    def initializeLocationWidthAndHeight(self):
        x, y = self.gameDisplay.get_size()
        self.locationWidth = x/self.environment.getGrid().getRows()
        self.locationHeight = y/self.environment.getGrid().getColumns()
    
    def addEntityToTrackedEntities(self, entity: Entity):
        self.entities[entity.getID()] = entity
        if isinstance(entity, LivingEntity):
            self.livingEntityIds.append(entity.getID())
        if type(entity) is Excrement:
            self.excrementIds.append(entity.getID())
        if type(entity) is BerryBush:
            self.berryBushIds.append(entity.getID())
            
    def generateInitialEntities(self):        
        for i in range(self.config.numWaterEntities):
            self.addEntityToTrackedEntities(Water())
        
        for i in range(self.config.numRockEntities):
            self.addEntityToTrackedEntities(Rock())
            
        for i in range(self.config.numGrassEntities):
            self.addEntityToTrackedEntities(Grass())
            
        for i in range(self.config.numBerriesEntities):
            self.addEntityToTrackedEntities(Berries())
            
        for i in range(self.config.numBerryBushEntities):
            self.addEntityToTrackedEntities(BerryBush())

        for i in range(self.config.numChickensToStart):
            self.addEntityToTrackedEntities(Chicken("Chicken"))

        for i in range(self.config.numPigsToStart):
            self.addEntityToTrackedEntities(Pig("Pig"))

        for i in range(self.config.numWolvesToStart):
            self.addEntityToTrackedEntities(Wolf("Wolf"))
        
        for i in range (self.config.numCowsToStart):
            self.addEntityToTrackedEntities(Cow("Cow"))
        
        for i in range(self.config.numFoxesToStart):
            self.addEntityToTrackedEntities(Fox("Fox"))

        for i in range(self.config.numRabbitsToStart):
            self.addEntityToTrackedEntities(Rabbit("Rabbit"))
    
    def placeInitialEntitiesInEnvironment(self):
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

    # private methods --------------------------------------------------------
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

    def performExcrementCheck(self, excrement):
        if self.shouldExcrementTurnIntoGrass(excrement):
            locationID = excrement.getLocationID()
            grid = self.environment.getGrid()
            location = grid.getLocation(locationID)
            
            self.removeEntity(excrement)
            grass = Grass()
            location.addEntity(grass)
            self.addEntityToTrackedEntities(grass)

    def growGrass(self):
        for excrementId in self.excrementIds:
            excrement = self.entities[excrementId]
            self.performExcrementCheck(excrement)

    def growBerries(self):
        for berryBushId in self.berryBushIds:
            berryBush = self.entities[berryBushId]
            if self.shouldBerryBushGainEnergy():
                berryBush.energy += 1
            berryBush.incrementTick()
            self.performBerryBushCheck(berryBush)

    def performBerryBushCheck(self, berryBush):
        if (berryBush.getTick() % self.config.berryBushGrowTime) != 0:
            return
        
        if berryBush.getEnergy() < 10:
            return
        
        locationID = berryBush.getLocationID()
        grid = self.environment.getGrid()
        location = grid.getLocation(locationID)
        
        numBerries = self.countBerriesInLocation(location)
        if numBerries >= 10:
            return
        
        berries = Berries()
        location.addEntity(berries)
        self.addEntityToTrackedEntities(berries)
        berryBush.energy = berryBush.getEnergy() // 2

    def countBerriesInLocation(self, location):
        count = 0
        for entityId in location.getEntities():
            entity = location.getEntity(entityId)
            if type(entity) is Berries:
                count += 1
        return count

    def initiateEntityActions(self):
        for entityId in self.livingEntityIds:
            entity = self.entities[entityId]
            self.moveActionHandler.initiateMoveAction(entity)
            if entity.needsEnergy():
                self.eatActionHandler.initiateEatAction(entity, self.removeEntity)
            else:
                if self.shouldEntityExcrete():
                    self.excreteActionHandler.initiateExcreteAction(entity, self.addEntityToTrackedEntities, self.numTicks)
                if self.shouldEntityReproduce():
                    self.reproduceActionHandler.initiateReproduceAction(entity, self.addEntityToTrackedEntities)

    def decreaseEnergyForLivingEntities(self):
        for entityId in self.livingEntityIds:
            entity = self.entities[entityId]
            entity.removeEnergy(1)
            if entity.getEnergy() <= 0:
                self.removeEntity(entity)
                
    def shouldExcrementTurnIntoGrass(self, excrement):
        return (self.numTicks - excrement.getTick()) > self.config.grassGrowTime

    def shouldBerryBushGainEnergy(self):
        return random.randrange(0, 100) < 10

    def shouldEntityExcrete(self):
        return random.randrange(0, 100) < (self.config.chanceToExcrete*100)
    
    def shouldEntityReproduce(self):
        return random.randrange(0, 100) < (self.config.chanceToReproduce*100)
