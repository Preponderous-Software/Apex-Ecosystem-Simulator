from entity import Entity


# @author Daniel McCoy Stephenson
# @since July 27th, 2022
class EatActionHandler:

    def __init__(self, environment):
        self.environment = environment
        self.debug = False
        self.energyCost = 1
        
    def initiateEatAction(self, entity: Entity, callbackFunction):
        # get location
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
        location = grid.getLocation(locationID)

        food = -1
        for e in location.getEntities():
            if entity.canEat(e):
                food = e
                break
        
        if food == -1:
            # no food found
            return

        callbackFunction(food)
        energy = food.getEnergy()
        entity.addEnergy(energy)

        # energy cost for action
        entity.removeEnergy(self.energyCost)

        if self.debug:
            print("[EVENT] ", entity.getName(), "ate", food.getName() , "at (", location.getX(), ",", location.getY(), ") and gained", energy, "energy.")