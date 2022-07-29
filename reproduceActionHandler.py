import random


# @author Daniel McCoy Stephenson
# @since July 27th, 2022
class ReproduceActionHandler:

    def __init__(self, environment):
        self.environment = environment
        self.debug = False
        
    def initiateReproduceAction(self, entity, callbackFunction):
        # get location
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
        location = grid.getLocation(locationID)

        mate = -1
        count = 0
        for e in location.getEntities():
            if type(e) is type(entity):
                count += 1
                if count == 2:
                    mate = e

        if count < 2:
            # no entity of this type found
            return

        entity.removeEnergy(1)
        mate.removeEnergy(1)

        name = random.randrange(0,9999)
        child = type(entity)(name)
        targetLocation = grid.getDown(location)
        if targetLocation == -1:
            return
        self.environment.addEntityToLocation(child, targetLocation)
        callbackFunction(child)

        if self.debug:
            print("[EVENT] ", entity.getName(), "has reproduced with", mate.getName() , "at (", location.getX(), ",", location.getY(), ").")