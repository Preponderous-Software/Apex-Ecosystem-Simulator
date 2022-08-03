from math import ceil
import random


# @author Daniel McCoy Stephenson
# @since July 28th, 2022
class Config:

    def __init__(self):
        # local
        grassFactor = random.randrange(2, 6)
        livingEntityFactor = 1.5
        minGridSize = 16
        maxGridSize = 32
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
        self.reinitializeConfigUponRestart = True
        self.limitTickSpeed = False

        # random
        self.gridSize = random.randrange(minGridSize, maxGridSize)
        self.grassGrowTime = random.randrange(minGrassGrowTime, maxGrassGrowTime)

        # calculated
        self.textSize = ceil(self.displayHeight/37)
        self.numGrassEntities = ceil(self.gridSize*self.gridSize*grassFactor)
        self.numChickensToStart = ceil(self.gridSize*livingEntityFactor/1)
        self.numPigsToStart = ceil(self.gridSize*livingEntityFactor/1)
        self.numCowsToStart = ceil(self.gridSize*livingEntityFactor/2)
        self.numWolvesToStart = ceil(self.gridSize*livingEntityFactor/8)
        self.numFoxesToStart = ceil(self.gridSize*livingEntityFactor/4)
        self.numRabbitsToStart = ceil(self.gridSize*livingEntityFactor/1)