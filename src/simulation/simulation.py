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
        self.environment = Environment(name, self.__config.gridSize)
        self.entities = dict()
        self.livingEntityIds = []
        self.running = True
        self.numTicks = 0
        
        self.__config = config
        self.__gameDisplay = gameDisplay
        self.__soundService = SoundService()

        self.__moveActionHandler = MoveActionHandler(self.environment)
        self.__eatActionHandler = EatActionHandler(self.environment)
        self.__excreteActionHandler = ExcreteActionHandler(self.environment)
        self.__reproduceActionHandler = ReproduceActionHandler(self.environment, self.__soundService, config)
        self.__excrementIds = []
        self.__berryBushIds = []

        self.initializeLocationWidthAndHeight()
    
    # public methods ---------------------------------------------------------
    def initializeLocationWidthAndHeight(self):
        x, y = self.__gameDisplay.get_size()
        self.locationWidth = x/self.environment.getGrid().getRows()
        self.locationHeight = y/self.environment.getGrid().getColumns()
    
    def addEntityToTrackedEntities(self, entity: Entity):
        self.entities[entity.getID()] = entity
        if isinstance(entity, LivingEntity):
            self.livingEntityIds.append(entity.getID())
        if type(entity) is Excrement:
            self.__excrementIds.append(entity.getID())
        if type(entity) is BerryBush:
            self.__berryBushIds.append(entity.getID())
            
    def generateInitialEntities(self):        
        for i in range(self.__config.numWaterEntities):
            self.addEntityToTrackedEntities(Water())
        
        for i in range(self.__config.numRockEntities):
            self.addEntityToTrackedEntities(Rock())
            
        for i in range(self.__config.numGrassEntities):
            self.addEntityToTrackedEntities(Grass())
            
        for i in range(self.__config.numBerriesEntities):
            self.addEntityToTrackedEntities(Berries())
            
        for i in range(self.__config.numBerryBushEntities):
            self.addEntityToTrackedEntities(BerryBush())

        for i in range(self.__config.numChickensToStart):
            self.addEntityToTrackedEntities(Chicken("Chicken"))

        for i in range(self.__config.numPigsToStart):
            self.addEntityToTrackedEntities(Pig("Pig"))

        for i in range(self.__config.numWolvesToStart):
            self.addEntityToTrackedEntities(Wolf("Wolf"))
        
        for i in range (self.__config.numCowsToStart):
            self.addEntityToTrackedEntities(Cow("Cow"))
        
        for i in range(self.__config.numFoxesToStart):
            self.addEntityToTrackedEntities(Fox("Fox"))

        for i in range(self.__config.numRabbitsToStart):
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
        return len(self.__excrementIds)
    
    def cleanup(self):
        print("---")
        print("State of environment:")
        self.environment.printInfo()
        print("Length of simulation:", self.numTicks, "ticks")
        print("---")
    
    def update(self):
        # initiate entity actions
        self.__initiateEntityActions()
        
        # decrease energy for living entities
        self.__decreaseEnergyForLivingEntities()
        
        # make grass grow
        self.__growGrass()

        # make berries grow
        self.__growBerries()

    # private methods --------------------------------------------------------
    def __removeEntityFromLocation(self, entity: Entity):
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
        location = grid.getLocation(locationID)
        if location.isEntityPresent(entity):
            location.removeEntity(entity)
            
    def __printDeathInfo(self, entity, oldestLivingEntity):
            toPrint = entity.getName() + " has died."
            if len(self.livingEntityIds) > 0:
                if entity.getID() == oldestLivingEntity.getID():
                    toPrint += " They were the oldest living entity."
            print(toPrint)
            
    def __removeEntity(self, entity: Entity):
        if len(self.livingEntityIds) > 0:
            oldestLivingEntityId = self.livingEntityIds[0]
            oldestLivingEntity = self.entities[oldestLivingEntityId]

        del self.entities[entity.getID()]
        self.__removeEntityFromLocation(entity)
        if isinstance(entity, LivingEntity):
            self.livingEntityIds.remove(entity.getID())
            self.__printDeathInfo(entity, oldestLivingEntity)
            if not self.__config.muted:
                self.__soundService.playDeathSoundEffect()
        if type(entity) is Excrement:
            self.__excrementIds.remove(entity.getID())
        if type(entity) is BerryBush:
            self.__berryBushIds.remove(entity.getID())

    def __performExcrementCheck(self, excrement):
        if self.__shouldExcrementTurnIntoGrass(excrement):
            locationID = excrement.getLocationID()
            grid = self.environment.getGrid()
            location = grid.getLocation(locationID)
            
            self.__removeEntity(excrement)
            grass = Grass()
            location.addEntity(grass)
            self.addEntityToTrackedEntities(grass)

    def __growGrass(self):
        for excrementId in self.__excrementIds:
            excrement = self.entities[excrementId]
            self.__performExcrementCheck(excrement)

    def __growBerries(self):
        for berryBushId in self.__berryBushIds:
            berryBush = self.entities[berryBushId]
            if self.__shouldBerryBushGainEnergy():
                berryBush.energy += 1
            berryBush.incrementTick()
            self.__performBerryBushCheck(berryBush)

    def __performBerryBushCheck(self, berryBush):
        if (berryBush.getTick() % self.__config.berryBushGrowTime) != 0:
            return
        
        if berryBush.getEnergy() < 10:
            return
        
        locationID = berryBush.getLocationID()
        grid = self.environment.getGrid()
        location = grid.getLocation(locationID)
        
        numBerries = self.__countBerriesInLocation(location)
        if numBerries >= 10:
            return
        
        berries = Berries()
        location.addEntity(berries)
        self.addEntityToTrackedEntities(berries)
        berryBush.energy = berryBush.getEnergy() // 2

    def __countBerriesInLocation(self, location):
        count = 0
        for entityId in location.getEntities():
            entity = location.getEntity(entityId)
            if type(entity) is Berries:
                count += 1
        return count

    def __initiateEntityActions(self):
        for entityId in self.livingEntityIds:
            entity = self.entities[entityId]
            self.__moveActionHandler.initiateMoveAction(entity)
            if entity.needsEnergy():
                self.__eatActionHandler.initiateEatAction(entity, self.__removeEntity)
            else:
                if self.__shouldEntityExcrete():
                    self.__excreteActionHandler.initiateExcreteAction(entity, self.addEntityToTrackedEntities, self.numTicks)
                if self.__shouldEntityReproduce():
                    self.__reproduceActionHandler.initiateReproduceAction(entity, self.addEntityToTrackedEntities)

    def __decreaseEnergyForLivingEntities(self):
        for entityId in self.livingEntityIds:
            entity = self.entities[entityId]
            entity.removeEnergy(1)
            if entity.getEnergy() <= 0:
                self.__removeEntity(entity)
                
    def __shouldExcrementTurnIntoGrass(self, excrement):
        return (self.numTicks - excrement.getTick()) > self.__config.grassGrowTime

    def __shouldBerryBushGainEnergy(self):
        return random.randrange(0, 100) < 10

    def __shouldEntityExcrete(self):
        return random.randrange(0, 100) < (self.__config.chanceToExcrete*100)
    
    def __shouldEntityReproduce(self):
        return random.randrange(0, 100) < (self.__config.chanceToReproduce*100)
