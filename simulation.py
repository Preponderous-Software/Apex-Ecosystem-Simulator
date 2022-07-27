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
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.displayWidth = 800
        self.displayHeight = 800
        self.gridSize = 10
        self.moveActionHandler = MoveActionHandler()

    def drawEnvironment(self, graphik, environment, locationWidth, locationHeight):
        for location in environment.getGrid().getLocations():
            color = self.white
            if location.getNumEntities() > 0:
                color = self.black
            graphik.drawRectangle(location.getX() * locationWidth, location.getY() * locationHeight, locationWidth, locationHeight, color)

    def run(self):
        pygame.init()
        gameDisplay = pygame.display.set_mode((self.displayWidth, self.displayHeight))
        graphik = Graphik(gameDisplay)
        pygame.display.set_caption("EWPELG")

        environment = Environment("Test", self.gridSize)
        gerald = Chicken("Gerald")
        paul = Chicken("Paul")
        grass = Grass()

        environment.addEntity(gerald)
        environment.addEntity(paul)
        environment.addEntity(grass)
        environment.printInfo()

        locationWidth = self.displayWidth/environment.getGrid().getRows()
        locationHeight = self.displayHeight/environment.getGrid().getColumns()

        running = True

        while running:
            # handle quitting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # white background to start
            gameDisplay.fill(self.white)

            # draw environment
            self.drawEnvironment(graphik, environment, locationWidth, locationHeight)

            # make entities move
            self.moveActionHandler.initiateMoveAction(gerald, environment)
            self.moveActionHandler.initiateMoveAction(paul, environment)

            # update and sleep
            pygame.display.update()
            time.sleep(0.5)