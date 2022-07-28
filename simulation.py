from math import ceil
from operator import truediv
import random
import time
import pygame
from chicken import Chicken
from eatActionHandler import EatActionHandler
from environment import Environment
from excrement import Excrement
from excreteActionHandler import ExcreteActionHandler
from graphik import Graphik
from grass import Grass
from moveActionHandler import MoveActionHandler
from pig import Pig


# @author Daniel McCoy Stephenson
# @since July 26th, 2022
class Simulation:

    def __init__(self):
        self.displayWidth = 600
        self.displayHeight = 600

        self.gridSize = 20

        self.numLivingEntities = ceil(self.gridSize/4)

        self.grassGrowTime = 100
        grassFactor = 1
        self.numGrassEntities = self.gridSize*self.gridSize*grassFactor

        self.tickSpeed = 0.001

        self.black = (0,0,0)
        self.white = (255,255,255)
        self.brown = (170, 120, 0)

        self.textSize = 20

        pygame.init()
        pygame.display.set_caption("Environment Simulation")

        self.gameDisplay = pygame.display.set_mode((self.displayWidth, self.displayHeight))
        self.graphik = Graphik(self.gameDisplay)
        
        self.environment = Environment("Test", self.gridSize)

        self.moveActionHandler = MoveActionHandler(self.environment)
        self.eatActionHandler = EatActionHandler(self.environment)
        self.excreteActionHandler = ExcreteActionHandler(self.environment)

        self.locationWidth = self.displayWidth/self.environment.getGrid().getRows()
        self.locationHeight = self.displayHeight/self.environment.getGrid().getColumns()

        self.livingEntities = []
        self.inanimateEntities = []

        self.running = True

        self.numTicks = 0
    
    def addInanimateEntity(self, entity):
        self.inanimateEntities.append(entity)
    
    def removeEntityFromLocation(self, entity):
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
        location = grid.getLocation(locationID)
        if location.isEntityPresent(entity):
            location.removeEntity(entity)

    def removeLivingEntity(self, entity):
        self.livingEntities.remove(entity)
        self.removeEntityFromLocation(entity)
    
    def removeInanimateEntity(self, entity):
        self.inanimateEntities.remove(entity)
        self.removeEntityFromLocation(entity)
        
    def drawEnvironment(self):
        for location in self.environment.getGrid().getLocations():
            color = self.brown
            if location.getNumEntities() > 0:
                color = location.getEntities()[-1].getColor()
            self.graphik.drawRectangle(location.getX() * self.locationWidth, location.getY() * self.locationHeight, self.locationWidth, self.locationHeight, color)

    def initializeEntities(self):
        for i in range(self.numLivingEntities):
            choice = random.randrange(0, 2)
            if (choice == 0):
                self.livingEntities.append(Chicken("Gerald"))
            elif choice == 1:
                self.livingEntities.append(Pig("Ulysses"))

        for i in range(self.numGrassEntities):
            self.inanimateEntities.append(Grass())

    def placeEntities(self):
        for entity in self.livingEntities:
            self.environment.addEntity(entity)
        for entity in self.inanimateEntities:
            self.environment.addEntity(entity)
    
    def displayStats(self):
        startingX = 100
        startingY = 50

        text = []

        text.append("Num ticks:")
        text.append(str(self.numTicks))
        text.append("")
        text.append("Living Entities: ")
        text.append(str(len(self.livingEntities)))
        text.append("")
        text.append("Inanimate Entities:")
        text.append(str(len(self.inanimateEntities)))


        buffer = self.textSize

        for i in range(0, len(text)):
            self.graphik.drawText(text[i], startingX, startingY + buffer*i, self.textSize, self.black)
        
    def checkForPotentialGrass(self):
        for entity in self.inanimateEntities:
            if type(entity) is Excrement and (self.numTicks - entity.getTick()) > self.grassGrowTime:
                locationID = entity.getLocationID()
                grid = self.environment.getGrid()
                location = grid.getLocation(locationID)
                
                self.removeInanimateEntity(entity)
                grass = Grass()
                location.addEntity(grass)
                self.addInanimateEntity(grass)

    
    def run(self):
        self.initializeEntities()
        self.placeEntities()

        self.environment.printInfo()

        while self.running:
            # handle quitting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()      

            # initiate entity actions
            for entity in self.livingEntities:
                if entity.getEnergy() <= 0:
                    self.removeLivingEntity(entity)
                    continue
                self.moveActionHandler.initiateMoveAction(entity)
                if entity.needsEnergy():
                    self.eatActionHandler.initiateEatAction(entity, Grass, self.removeInanimateEntity)
                else:
                    if random.randrange(0, 4) == 0:
                        self.excreteActionHandler.initiateExcreteAction(entity, self.addInanimateEntity, self.numTicks)
            
            # decrease energy for living entities
            for entity in self.livingEntities:
                entity.removeEnergy(1)
            
            self.checkForPotentialGrass()

            # draw environment
            self.drawEnvironment()

            self.displayStats()

            # update and sleep
            pygame.display.update()
            time.sleep(self.tickSpeed)
            self.numTicks += 1

            if len(self.livingEntities) == 0:
                time.sleep(10)
                self.running = False
                print("State of environment:")
                self.environment.printInfo()
                print("Length of simulation:", self.numTicks, "ticks")