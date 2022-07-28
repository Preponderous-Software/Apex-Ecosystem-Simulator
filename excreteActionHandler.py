import random

from excrement import Excrement


# @author Daniel McCoy Stephenson
# @since July 27th, 2022
class ExcreteActionHandler:

    def __init__(self, environment):
        self.environment = environment
        self.debug = False
        
    def initiateExcreteAction(self, entity, callbackFunction, tick):
        # get location
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
        location = grid.getLocation(locationID)
        excretionLocation = grid.getUp(location)
        excrement = Excrement(tick)
        if (excretionLocation == -1):
            location.addEntity(excrement)
        else:
            excretionLocation.addEntity(excrement)
            callbackFunction(excrement)