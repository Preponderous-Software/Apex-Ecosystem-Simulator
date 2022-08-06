from math import ceil
import random


# @author Daniel McCoy Stephenson
# @since July 28th, 2022
class Config:
    def __init__(self):
        # local
        grassFactor = random.randrange(3, 10)
        livingEntityFactor = 0.2
        minGridSize = 8
        maxGridSize = 36
        minGrassGrowTime = 100
        maxGrassGrowTime = 300
        chickenFactor = random.randrange(1, 10)
        pigFactor = random.randrange(0, 10)
        cowFactor = random.randrange(0, 10)
        wolfFactor = random.randrange(0, 5)
        foxFactor = random.randrange(0, 5)
        rabbitFactor = random.randrange(0, 10)

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
        self.localView = False
        self.highlightOldestEntity = False
        self.highlightColor = (255, 255, 0)
        self.localViewSize = 2
        self.fullscreen = False

        # random
        self.gridSize = random.randrange(minGridSize, maxGridSize)
        self.grassGrowTime = random.randrange(minGrassGrowTime, maxGrassGrowTime)

        # calculated
        self.textSize = ceil(self.displayHeight/37)
        self.numGrassEntities = ceil(self.gridSize*self.gridSize*grassFactor)
        self.numChickensToStart = ceil(self.gridSize*livingEntityFactor*chickenFactor)
        self.numPigsToStart = ceil(self.gridSize*livingEntityFactor*pigFactor)
        self.numCowsToStart = ceil(self.gridSize*livingEntityFactor*cowFactor)
        self.numWolvesToStart = ceil(self.gridSize*livingEntityFactor*wolfFactor)
        self.numFoxesToStart = ceil(self.gridSize*livingEntityFactor*foxFactor)
        self.numRabbitsToStart = ceil(self.gridSize*livingEntityFactor*rabbitFactor)
        self.maxLocalViewSize = maxGridSize/4