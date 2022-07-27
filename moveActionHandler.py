import random


# @author Daniel McCoy Stephenson
# @since July 26th, 2022
class MoveActionHandler:

    def __init__(self, environment):
        self.environment = environment

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
        
    def initiateMoveAction(self, entity):
        # get location
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
        location = grid.getLocation(locationID) 
        
        # get new location
        newLocation = self.chooseRandomDirection(grid, location)
        if newLocation == -1:
            return
        
        # move entity
        location.removeEntity(entity)
        newLocation.addEntity(entity)

        print("[EVENT] ", entity.getName(), "moved to (", location.getX(), ",", location.getY(), ")")