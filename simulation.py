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
        self.environment = Environment("Test", 100)
        self.moveActionHandler = MoveActionHandler(self.environment)

        self.black = (0,0,0)
        self.white = (255,255,255)

        self.locationWidth = self.displayWidth/self.environment.getGrid().getRows()
        self.locationHeight = self.displayHeight/self.environment.getGrid().getColumns()

    def drawEnvironment(self):
        for location in self.environment.getGrid().getLocations():
            color = self.white
            if location.getNumEntities() > 0:
                color = location.getEntities()[-1].getColor()
            self.graphik.drawRectangle(location.getX() * self.locationWidth, location.getY() * self.locationHeight, self.locationWidth, self.locationHeight, color)

    def run(self):
        gerald = Chicken("Gerald")
        paul = Chicken("Paul")
        grass1 = Grass()
        grass2 = Grass()
        grass3 = Grass()

        self.environment.addEntity(gerald)
        self.environment.addEntity(paul)
        self.environment.addEntity(grass1)
        self.environment.addEntity(grass2)
        self.environment.addEntity(grass3)
        self.environment.printInfo()

        running = True
        while running:
            # handle quitting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()            

            # make entities moves
            self.moveActionHandler.initiateMoveAction(gerald)
            self.moveActionHandler.initiateMoveAction(paul)

            # draw environment
            self.gameDisplay.fill(self.white)
            self.drawEnvironment()

            # update and sleep
            pygame.display.update()
            time.sleep(0.5)