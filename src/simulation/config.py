from math import ceil
import random


# @author Daniel McCoy Stephenson
# @since July 28th, 2022
class Config:
    def __init__(self):
        # locally used
        self.grassFactor = random.randrange(3, 10)
        self.livingEntityFactor = 0.2
        self.minGridSize = 8
        self.maxGridSize = 24
        self.minGrassGrowTime = 100
        self.maxGrassGrowTime = 300
        self.chickenFactor = random.randrange(1, 10)
        self.pigFactor = random.randrange(0, 10)
        self.cowFactor = random.randrange(0, 10)
        self.wolfFactor = random.randrange(0, 5)
        self.foxFactor = random.randrange(0, 5)
        self.rabbitFactor = random.randrange(0, 10)

        # static
        self.setStaticValues()

        # random
        self.randomizeGridSize()
        self.randomizeGrassGrowTime()

        # calculated
        self.calculateValues()
    
    def setStaticValues(self):
        self.displayWidth = 400
        self.displayHeight = 400
        self.tickSpeed = 5
        self.maxTickSpeed = 10
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.brown = (170, 120, 0)
        self.endSimulationUponAllLivingEntitiesDying = True
        self.autoRestart = True
        self.chanceToExcrete = 0.10
        self.chanceToReproduce = 0.02
        self.randomizeGridSizeUponRestart = True
        self.limitTickSpeed = True
        self.localView = False
        self.highlightOldestEntity = False
        self.highlightColor = (255, 255, 0)
        self.localViewSize = 2
        self.fullscreen = False
        self.muted = False
    
    def randomizeGridSize(self):
        self.gridSize = random.randrange(self.minGridSize, self.maxGridSize)
    
    def randomizeGrassGrowTime(self):
        self.grassGrowTime = random.randrange(self.minGrassGrowTime, self.maxGrassGrowTime)

    def calculateValues(self):
        self.textSize = ceil(self.displayHeight/37)
        self.numGrassEntities = ceil(self.gridSize*self.gridSize*self.grassFactor)
        self.numChickensToStart = ceil(self.gridSize*self.livingEntityFactor*self.chickenFactor)
        self.numPigsToStart = ceil(self.gridSize*self.livingEntityFactor*self.pigFactor)
        self.numCowsToStart = ceil(self.gridSize*self.livingEntityFactor*self.cowFactor)
        self.numWolvesToStart = ceil(self.gridSize*self.livingEntityFactor*self.wolfFactor)
        self.numFoxesToStart = ceil(self.gridSize*self.livingEntityFactor*self.foxFactor)
        self.numRabbitsToStart = ceil(self.gridSize*self.livingEntityFactor*self.rabbitFactor)
        self.maxLocalViewSize = self.maxGridSize/4