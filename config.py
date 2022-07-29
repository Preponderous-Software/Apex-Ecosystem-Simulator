from math import ceil
import random


# @author Daniel McCoy Stephenson
# @since July 28th, 2022
class Config:

    def __init__(self):
        # local
        grassFactor = random.randrange(1, 5)
        livingEntityFactor = 1
        minGridSize = 4
        maxGridSize = 40
        minGrassGrowTime = 100
        maxGrassGrowTime = 200

        # static
        self.displayWidth = 720
        self.displayHeight = 720
        self.tickSpeed = 1
        self.maxTickSpeed = 10
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.brown = (170, 120, 0)
        self.textSize = 20
        self.endSimulationUponAllLivingEntitiesDying = True
        self.autoRestart = True
        self.chanceToExcrete = 0.10
        self.chanceToReproduce = 0.10

        # calculated/random
        self.gridSize = random.randrange(minGridSize, maxGridSize)
        self.numLivingEntities = ceil(self.gridSize*livingEntityFactor)
        self.grassGrowTime = random.randrange(minGrassGrowTime, maxGrassGrowTime)
        self.numGrassEntities = self.gridSize*self.gridSize*grassFactor