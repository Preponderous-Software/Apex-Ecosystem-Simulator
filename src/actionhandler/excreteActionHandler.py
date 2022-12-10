import random
from lib.pyenvlib.entity import Entity
from lib.pyenvlib.grid import Grid
from lib.pyenvlib.location import Location

from entity.excrement import Excrement


# @author Daniel McCoy Stephenson
# @since July 27th, 2022
class ExcreteActionHandler:

    def __init__(self, environment):
        self.environment = environment
        self.debug = False
        self.energyCost = 1
    
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
        for e in location.getEntities():
            if e.isSolid():
                return True
        return False
        
    def initiateExcreteAction(self, entity: Entity, callbackFunction, tick):
        # get location
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
        location = grid.getLocation(locationID)
        excretionLocation = self.getRandomDirection(grid, location)
        excrement = Excrement(tick)
        if (excretionLocation == -1 or self.isLocationImpassible(excretionLocation)):
            location.addEntity(excrement)
        else:
            excretionLocation.addEntity(excrement)
            callbackFunction(excrement)
        
        # energy cost for action
        entity.removeEnergy(self.energyCost)