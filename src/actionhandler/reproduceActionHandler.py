import random

from lib.pyenvlib.entity import Entity
from lib.pyenvlib.environment import Environment
from lib.pyenvlib.grid import Grid
from lib.pyenvlib.location import Location

from simulation.config import Config
from service.soundService import SoundService


# @author Daniel McCoy Stephenson
# @since July 27th, 2022
class ReproduceActionHandler:

    def __init__(self, environment: Environment, soundService: SoundService, config: Config):
        self.environment = environment
        self.childCount = 0
        self.energyCost = 1
        self.soundService = soundService
        self.config = config
    
    def getRandomDirection(self, grid: Grid, location: Location):
        direction = random.randrange(0, 4)
        if direction == 0:
            return grid.getUp(location)
        elif direction == 1:
            return grid.getRight(location)
        elif direction == 2:
            return grid.getDown(location)
        elif direction == 3:
            return grid.getLeft(location)
    
    def isLocationImpassible(self, location: Location):
        # search current location
        for eid in location.getEntities():
            entity = location.getEntities()[eid]
            if entity.isSolid():
                return True
        return False
        
    def initiateReproduceAction(self, entity: Entity, callbackFunction):
        # get location
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
        location = grid.getLocation(locationID)

        mate = -1
        for eid in location.getEntities():
            targetEntity = location.getEntities()[eid]
            if type(targetEntity) is type(entity) and targetEntity.getID() is not entity.getID():
                mate = targetEntity

        if mate == -1:
            # no entity of this type found
            return

        # energy cost for action
        entity.removeEnergy(self.energyCost)
        mate.removeEnergy(self.energyCost)

        name = "child " + str(self.childCount)
        child = type(entity)(name)
        targetLocation = self.getRandomDirection(grid, location)
        if targetLocation == -1 or self.isLocationImpassible(targetLocation):
            targetLocation = location
            return
        self.environment.addEntityToLocation(child, targetLocation)
        callbackFunction(child)
        
        if not self.config.muted:
            self.soundService.playReproduceSoundEffect()

        self.childCount += 1

        print(entity.getName(), "has reproduced with", mate.getName() , "at (", location.getX(), ",", location.getY(), ").")