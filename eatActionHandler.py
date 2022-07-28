import random


# @author Daniel McCoy Stephenson
# @since July 27th, 2022
class EatActionHandler:

    def __init__(self, environment):
        self.environment = environment
        self.debug = False
        
    def initiateEatAction(self, entity, foodType, callbackFunction):
        # get location
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
        location = grid.getLocation(locationID)

        food = -1
        for e in location.getEntities():
            if type(e) is foodType:
                food = e
                break
        
        if food == -1:
            # no food of this type found
            return

        location.removeEntity(food)
        callbackFunction(food)
        energy = food.getEnergy()
        entity.addEnergy(energy)

        if self.debug:
            print("[EVENT] ", entity.getName(), "ate", food.getName() , "at (", location.getX(), ",", location.getY(), ") and gained", energy, "energy.")