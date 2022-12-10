from lib.pyenvlib.entity import Entity


# @author Daniel McCoy Stephenson
# @since August 5th, 2022
class DrawableEntity(Entity):
    def __init__(self, name, color, solid):
        Entity.__init__(self, name)
        self.color = color
        self.solid = solid
        
    # Returns the color of the entity.
    def getColor(self):
        return self.color
    
    def isSolid(self):
        return self.solid