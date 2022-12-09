import random
from config import Config
from pyenvlib.entity import Entity
from pyenvlib.environment import Environment
from pyenvlib.grid import Grid
from pyenvlib.location import Location
from soundService import SoundService


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
        
    def initiateReproduceAction(self, entity: Entity, callbackFunction):
        # get location
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
        location = grid.getLocation(locationID)

        mate = -1
        for e in location.getEntities():
            if type(e) is type(entity) and e.getID() is not entity.getID():
                mate = e

        if mate == -1:
            # no entity of this type found
            return

        # energy cost for action
        entity.removeEnergy(self.energyCost)
        mate.removeEnergy(self.energyCost)

        name = "child " + str(self.childCount)
        child = type(entity)(name)
        targetLocation = self.getRandomDirection(grid, location)
        if targetLocation == -1:
            return
        self.environment.addEntityToLocation(child, targetLocation)
        callbackFunction(child)
        
        if not self.config.muted:
            self.soundService.playReproduceSoundEffect()

        self.childCount += 1

        print(entity.getName(), "has reproduced with", mate.getName() , "at (", location.getX(), ",", location.getY(), ").")