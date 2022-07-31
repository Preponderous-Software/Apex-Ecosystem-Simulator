import random

from excrement import Excrement


# @author Daniel McCoy Stephenson
# @since July 27th, 2022
class ExcreteActionHandler:

    def __init__(self, environment):
        self.environment = environment
        self.debug = False
    
    def getRandomDirection(self, grid, location):
        direction = random.randrange(0, 4)
        if direction == 0:
            return grid.getUp(location)
        elif direction == 1:
            return grid.getRight(location)
        elif direction == 2:
            return grid.getDown(location)
        elif direction == 3:
            return grid.getLeft(location)
        
    def initiateExcreteAction(self, entity, callbackFunction, tick):
        # get location
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
        location = grid.getLocation(locationID)
        excretionLocation = self.getRandomDirection(grid, location)
        excrement = Excrement(tick)
        if (excretionLocation == -1):
            location.addEntity(excrement)
        else:
            excretionLocation.addEntity(excrement)
            callbackFunction(excrement)