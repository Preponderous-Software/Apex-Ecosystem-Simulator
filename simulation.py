from math import ceil
from operator import truediv
import random
import time
import pygame
from chicken import Chicken
from config import Config
from eatActionHandler import EatActionHandler
from environment import Environment
from excrement import Excrement
from excreteActionHandler import ExcreteActionHandler
from graphik import Graphik
from grass import Grass
from moveActionHandler import MoveActionHandler
from pig import Pig
from reproduceActionHandler import ReproduceActionHandler
from wolf import Wolf


# @author Daniel McCoy Stephenson
# @since July 26th, 2022
class Simulation:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Environment Simulation")

        self.config = Config()

        self.gameDisplay = pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight))
        self.graphik = Graphik(self.gameDisplay)
        
        self.environment = Environment("Test", self.config.gridSize)

        self.moveActionHandler = MoveActionHandler(self.environment)
        self.eatActionHandler = EatActionHandler(self.environment)
        self.excreteActionHandler = ExcreteActionHandler(self.environment)
        self.reproduceActionHandler = ReproduceActionHandler(self.environment)

        self.locationWidth = self.config.displayWidth/self.environment.getGrid().getRows()
        self.locationHeight = self.config.displayHeight/self.environment.getGrid().getColumns()

        self.livingEntities = []
        self.inanimateEntities = []

        self.running = True

        self.numTicks = 0

        self.debug = False
    
    def addLivingEntity(self, entity):
        self.livingEntities.append(entity)
    
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
            color = self.config.brown
            if location.getNumEntities() > 0:
                color = location.getEntities()[-1].getColor()
            self.graphik.drawRectangle(location.getX() * self.locationWidth, location.getY() * self.locationHeight, self.locationWidth, self.locationHeight, color)

    def initializeEntities(self):
        for i in range(self.config.numLivingEntities):
            choice = random.randrange(0, 3)
            if (choice == 0):
                self.addLivingEntity(Chicken("Chicken"))
            elif choice == 1:
                self.addLivingEntity(Pig("Pig"))
            elif choice == 2:
                self.addLivingEntity(Wolf("Wolf"))

        for i in range(self.config.numGrassEntities):
            self.addInanimateEntity(Grass())

    def placeEntities(self):
        for entity in self.livingEntities:
            self.environment.addEntity(entity)
        for entity in self.inanimateEntities:
            self.environment.addEntity(entity)
    
    def getNumberOfLivingEntitiesOfType(self, entityType):
        count = 0
        for entity in self.livingEntities:
            if type(entity) is entityType:
                count += 1
        return count
    
    def getNumberOfInanimateEntitiesOfType(self, entityType):
        count = 0
        for entity in self.inanimateEntities:
            if type(entity) is entityType:
                count += 1
        return count
    
    def displayStats(self):
        startingX = 100
        startingY = 50

        text = []

        text.append("Tick Speed:")
        text.append(str(self.config.tickSpeed))
        text.append("")
        text.append("Num Ticks:")
        text.append(str(self.numTicks))
        text.append("")
        text.append("Living Entities: ")
        text.append(str(len(self.livingEntities)))
        text.append("")
        text.append("Inanimate Entities:")
        text.append(str(len(self.inanimateEntities)))
        text.append("")
        text.append("Grass:")
        text.append(str(self.getNumberOfInanimateEntitiesOfType(Grass)))
        text.append("")
        text.append("Excrement:")
        text.append(str(self.getNumberOfInanimateEntitiesOfType(Excrement)))
        text.append("")
        text.append("Chickens:")
        text.append(str(self.getNumberOfLivingEntitiesOfType(Chicken)))
        text.append("")
        text.append("Pigs:")
        text.append(str(self.getNumberOfLivingEntitiesOfType(Pig)))
        text.append("")
        text.append("Wolves:")
        text.append(str(self.getNumberOfLivingEntitiesOfType(Wolf)))


        buffer = self.config.textSize

        for i in range(0, len(text)):
            self.graphik.drawText(text[i], startingX, startingY + buffer*i, self.config.textSize, self.config.black)
        
    def checkForPotentialGrass(self):
        for entity in self.inanimateEntities:
            if type(entity) is Excrement and (self.numTicks - entity.getTick()) > self.config.grassGrowTime:
                locationID = entity.getLocationID()
                grid = self.environment.getGrid()
                location = grid.getLocation(locationID)
                
                self.removeInanimateEntity(entity)
                grass = Grass()
                location.addEntity(grass)
                self.addInanimateEntity(grass)

    def handleKeyDownEvent(self, key):
        if key == pygame.K_d:
            if self.debug == True:
                self.debug = False
            else:
                self.debug = True
        if key == pygame.K_q:
            self.running = False
        if key == pygame.K_r:
            self.cleanup()
            return "restart"
        if key == pygame.K_c:
            chicken = Chicken("player created chicken")
            self.environment.addEntity(chicken)
            self.addLivingEntity(chicken)
        if key == pygame.K_p:
            pig = Pig("player created pig")
            self.environment.addEntity(pig)
            self.addLivingEntity(pig)
        if key == pygame.K_w:
            wolf = Wolf("player created wolf")
            self.environment.addEntity(wolf)
            self.addLivingEntity(wolf)
        if key == pygame.K_UP:
            if self.config.tickSpeed < self.config.maxTickSpeed:
                self.config.tickSpeed += 1
        if key == pygame.K_DOWN:
            if self.config.tickSpeed > 1:
                self.config.tickSpeed -= 1

    def initiateEntityActions(self):
        for entity in self.livingEntities:
            self.moveActionHandler.initiateMoveAction(entity)
            if entity.needsEnergy():
                foodType = -1
                if type(entity) is Chicken:
                    foodType = Grass
                    self.eatActionHandler.initiateEatAction(entity, foodType, self.removeInanimateEntity)
                elif type(entity) is Pig:
                    foodType = Chicken
                    self.eatActionHandler.initiateEatAction(entity, foodType, self.removeLivingEntity)
                elif type(entity) is Wolf:
                    foodType = Pig
                    self.eatActionHandler.initiateEatAction(entity, foodType, self.removeLivingEntity)
                else:
                    return
            else:
                if random.randrange(0, 100) < (self.config.chanceToExcrete*100):
                    self.excreteActionHandler.initiateExcreteAction(entity, self.addInanimateEntity, self.numTicks)
                if random.randrange(0, 100) < (self.config.chanceToReproduce*100):
                    self.reproduceActionHandler.initiateReproduceAction(entity, self.addLivingEntity)
    
    def decreaseEnergyForLivingEntities(self):
        for entity in self.livingEntities:
            entity.removeEnergy(1)
            if entity.getEnergy() <= 0:
                self.removeLivingEntity(entity)
    
    def cleanup(self):
        print("---")
        print("State of environment:")
        self.environment.printInfo()
        print("Length of simulation:", self.numTicks, "ticks")
        print("---")
    
    def quit(self):
        pygame.quit()
        quit()
    
    def run(self):
        self.initializeEntities()
        self.placeEntities()

        self.environment.printInfo()

        while self.running:
            for event in pygame.event.get():
                # handle quitting
                if event.type == pygame.QUIT:
                    self.cleanup()
                    self.quit()
                # handle key down
                if event.type == pygame.KEYDOWN:
                    result = self.handleKeyDownEvent(event.key)
                    if result == "restart":
                        self.cleanup()
                        return "restart"

            # initiate entity actions
            self.initiateEntityActions()
            
            # decrease energy for living entities
            self.decreaseEnergyForLivingEntities()
            
            # make grass grow
            self.checkForPotentialGrass()

            # draw environment
            self.drawEnvironment()
            if self.debug:
                self.displayStats()

            # update and sleep
            pygame.display.update()
            time.sleep((self.config.maxTickSpeed - self.config.tickSpeed)/self.config.maxTickSpeed)
            self.numTicks += 1

            if (self.config.endSimulationUponAllLivingEntitiesDying):
                if len(self.livingEntities) == 0:
                    self.running = False
                    time.sleep(1)
                    if (self.config.autoRestart):
                        self.cleanup()
                        return "restart"