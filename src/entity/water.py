import random
from entity.drawableEntity import DrawableEntity


# @author Daniel McCoy Stephenson
# @since December 8th, 2022
class Water(DrawableEntity):
    def __init__(self):
        DrawableEntity.__init__(self, "Water", (66, 194, 229))