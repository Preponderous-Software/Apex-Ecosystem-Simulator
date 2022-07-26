from operator import truediv
import pygame
from chicken import Chicken
from environment import Environment
from graphik import Graphik

black = (0,0,0)
white = (255,255,255)

displayWidth = 800
displayHeight = 800

gridSize = 4

def drawEnvironment(graphik, environment, locationWidth, locationHeight):
    for location in environment.getGrid().getLocations():
        color = white
        if location.getNumEntities() > 0:
            color = black
        graphik.drawRectangle(location.getX() * locationWidth, location.getY() * locationHeight, locationWidth, locationHeight, color)\

def main():
    pygame.init()
    gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
    graphik = Graphik(gameDisplay)
    pygame.display.set_caption("EWPELG")

    environment = Environment("Test", gridSize)
    chicken = Chicken("Gerald")

    environment.addEntity(chicken)
    environment.printInfo()

    locationWidth = displayWidth/environment.getGrid().getRows()
    locationHeight = displayHeight/environment.getGrid().getColumns()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            gameDisplay.fill(white)
            drawEnvironment(graphik, environment, locationWidth, locationHeight)
            pygame.display.update()

main()