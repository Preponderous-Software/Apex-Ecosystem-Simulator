from math import ceil
import random


# @author Daniel McCoy Stephenson
# @since July 28th, 2022
class Config:

    def __init__(self):
        # local
        grassFactor = random.randrange(1, 5)
        livingEntityFactor = 1
        minGridSize = 20
        maxGridSize = 40
        minGrassGrowTime = 100
        maxGrassGrowTime = 500

        # static
        self.displayWidth = 400
        self.displayHeight = 400
        self.tickSpeed = 1
        self.maxTickSpeed = 10
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.brown = (170, 120, 0)
        self.endSimulationUponAllLivingEntitiesDying = True
        self.autoRestart = True
        self.chanceToExcrete = 0.10
        self.chanceToReproduce = 0.02

        # calculated/random
        self.gridSize = random.randrange(minGridSize, maxGridSize)
        self.textSize = ceil(self.displayHeight/37)
        self.numChickensToStart = ceil(self.gridSize*livingEntityFactor/1)
        self.numPigsToStart = ceil(self.gridSize*livingEntityFactor/2)
        self.numCowsToStart = ceil(self.gridSize*livingEntityFactor/4)
        self.numWolvesToStart = ceil(self.gridSize*livingEntityFactor/8)
        self.grassGrowTime = random.randrange(minGrassGrowTime, maxGrassGrowTime)
        self.numGrassEntities = self.gridSize*self.gridSize*grassFactor