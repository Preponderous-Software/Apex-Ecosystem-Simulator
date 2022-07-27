from operator import truediv
import random
import pygame
from chicken import Chicken
from environment import Environment
from graphik import Graphik
from grass import Grass


# @author Daniel McCoy Stephenson
# @since July 26th, 2022
class Simulation:

    def __init__(self):
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.displayWidth = 800
        self.displayHeight = 800
        self.gridSize = 10

    def moveEntity(self, entity, environment):
        locationID = entity.getLocationID()
        grid = environment.getGrid()
        location = grid.getLocation(locationID) 
        direction = random.randrange(0, 4)

        if direction == 0:
            newLocation = grid.getUp(location)
        elif direction == 1:
            newLocation = grid.getRight(location)
        elif direction == 2:
            newLocation = grid.getDown(location)
        elif direction == 3:
            newLocation = grid.getLeft(location)

        if newLocation == -1:
            return
        
        location.removeEntity(entity)
        newLocation.addEntity(entity)

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                gameDisplay.fill(self.white)
                self.drawEnvironment(graphik, environment, locationWidth, locationHeight)
                self.moveEntity(gerald, environment)
                self.moveEntity(paul, environment)
                pygame.display.update()