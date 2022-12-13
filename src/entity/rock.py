import random
from entity.drawableEntity import DrawableEntity


# @author Daniel McCoy Stephenson
# @since December 12th, 2022
class Rock(DrawableEntity):
    def __init__(self):
        DrawableEntity.__init__(self, "Rock", (random.randrange(100, 110), random.randrange(100, 110), random.randrange(100, 110)), True)