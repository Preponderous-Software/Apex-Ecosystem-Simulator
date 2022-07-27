from operator import truediv
import random
import time
import pygame
from chicken import Chicken
from environment import Environment
from graphik import Graphik
from grass import Grass
from moveActionHandler import MoveActionHandler


# @author Daniel McCoy Stephenson
# @since July 26th, 2022
class Simulation:

    def __init__(self):
        self.displayWidth = 800
        self.displayHeight = 800

        pygame.init()
        pygame.display.set_caption("Environment Simulation")

        self.gameDisplay = pygame.display.set_mode((self.displayWidth, self.displayHeight))
        self.graphik = Graphik(self.gameDisplay)
        self.environment = Environment("Test", 16)
        self.moveActionHandler = MoveActionHandler(self.environment)

        self.black = (0,0,0)
        self.white = (255,255,255)

        self.locationWidth = self.displayWidth/self.environment.getGrid().getRows()
        self.locationHeight = self.displayHeight/self.environment.getGrid().getColumns()

        self.livingEntities = []
        self.inanimateEntities = []

        self.running = True
        self.tickSpeed = 1

    def drawEnvironment(self):
        for location in self.environment.getGrid().getLocations():
            color = self.white
            if location.getNumEntities() > 0:
                color = location.getEntities()[-1].getColor()
            self.graphik.drawRectangle(location.getX() * self.locationWidth, location.getY() * self.locationHeight, self.locationWidth, self.locationHeight, color)

    def initializeEntities(self):
        self.livingEntities.append(Chicken("Gerald"))
        self.livingEntities.append(Chicken("Paul"))
        self.inanimateEntities.append(Grass())
        self.inanimateEntities.append(Grass())
        self.inanimateEntities.append(Grass())

    def placeEntities(self):
        for entity in self.livingEntities:
            self.environment.addEntity(entity)
        for entity in self.inanimateEntities:
            self.environment.addEntity(entity)

    def run(self):
        self.initializeEntities()
        self.placeEntities()
        while self.running:
            # handle quitting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()            

            # make entities moves
            for entity in self.livingEntities:
                self.moveActionHandler.initiateMoveAction(entity)

            # draw environment
            self.gameDisplay.fill(self.white)
            self.drawEnvironment()

            # update and sleep
            pygame.display.update()
            time.sleep(self.tickSpeed)