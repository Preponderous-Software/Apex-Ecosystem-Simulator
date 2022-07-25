from operator import truediv
import random
import pygame
from environment import Environment
from graphik import Graphik


pygame.init()

black = (0,0,0)
white = (255,255,255)

displayWidth = 1080
displayHeight = 720

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))

graphik = Graphik(gameDisplay)

pygame.display.set_caption("EWPELG")

clock = pygame.time.Clock()

environment = Environment("Test", 100)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        gameDisplay.fill(white)

        locationWidth = displayWidth/environment.getGrid().getRows()
        locationHeight = displayHeight/environment.getGrid().getColumns()

        # draw environment
        for location in environment.getGrid().getLocations():
            red = random.randrange(50, 200)
            green = random.randrange(50, 200)
            blue = random.randrange(50, 200)
            graphik.drawRectangle(location.getX() * locationWidth, location.getY() * locationHeight, locationWidth, locationHeight, (red,green,blue))
        
        pygame.display.update()