from math import ceil
import random


# @author Daniel McCoy Stephenson
# @since July 28th, 2022
class Config:

    def __init__(self):
        # local
        grassFactor = random.randrange(1, 5)
        livingEntityFactor = 1
        minGridSize = 10
        maxGridSize = 20
        minGrassGrowTime = 100
        maxGrassGrowTime = 500

        # static
        self.displayWidth = 600
        self.displayHeight = 600
        self.tickSpeed = 1
        self.maxTickSpeed = 10
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.brown = (170, 120, 0)
        self.textSize = 20
        self.endSimulationUponAllLivingEntitiesDying = True
        self.autoRestart = True
        self.chanceToExcrete = 0.10
        self.chanceToReproduce = 0.02
        # calculated/random
        self.gridSize = random.randrange(minGridSize, maxGridSize)
        self.numChickensToStart = ceil(self.gridSize*livingEntityFactor/1)
        self.numPigsToStart = ceil(self.gridSize*livingEntityFactor/2)
        self.numWolvesToStart = ceil(self.gridSize*livingEntityFactor/4)
        self.grassGrowTime = random.randrange(minGrassGrowTime, maxGrassGrowTime)
        self.numGrassEntities = self.gridSize*self.gridSize*grassFactor