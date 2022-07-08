from chicken import Chicken
from environment import Environment
from grass import Grass


environment = Environment("Test")

grass = Grass()
chicken = Chicken("Gerald")

environment.addEntity(grass)
environment.addEntity(chicken)

environment.printInfo()