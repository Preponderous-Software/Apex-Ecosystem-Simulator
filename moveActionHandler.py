import random

from grass import Grass


# @author Daniel McCoy Stephenson
# @since July 26th, 2022
class MoveActionHandler:

    def __init__(self, environment):
        self.environment = environment
        self.debug = False

    def chooseRandomDirection(self, grid, location):
        direction = random.randrange(0, 4)
        if direction == 0:
            return grid.getUp(location)
        elif direction == 1:
            return grid.getRight(location)
        elif direction == 2:
            return grid.getDown(location)
        elif direction == 3:
            return grid.getLeft(location)
        
    def searchForFood(self, entity, grid, location):
        attempts = 0
        while attempts < random.randrange(1, 5):
            searchLocation = self.chooseRandomDirection(grid, location)
            if searchLocation == -1:
                continue
            for e in searchLocation.getEntities():
                if entity.canEat(e):
                    return searchLocation
            attempts += 1
        return -1
        
    def initiateMoveAction(self, entity):
        # get location
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
        location = grid.getLocation(locationID)
        
        # return if we don't need energy
        if not entity.needsEnergy():
            return

        # get new location
        newLocation = self.searchForFood(entity, grid, location)
        if newLocation == -1:
            # no food found
            newLocation = self.chooseRandomDirection(grid, location)
            
        if newLocation == -1:
            # location doesn't exist, we're at a border
            return
        
        # move entity
        location.removeEntity(entity)
        newLocation.addEntity(entity)

        if self.debug:
            print("[EVENT] ", entity.getName(), "moved to (", location.getX(), ",", location.getY(), ")")