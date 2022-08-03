import time
import pygame
from chicken import Chicken
from config import Config
from cow import Cow
from excrement import Excrement
from fox import Fox
from graphik import Graphik
from grass import Grass
from pig import Pig
from simulation import Simulation
from wolf import Wolf


# @author Daniel McCoy Stephenson
# @since July 31st, 2022
class Apex:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Apex")

        self.config = Config()

        self.gameDisplay = pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.RESIZABLE)
        pygame.display.set_icon(pygame.image.load('icon.PNG'))
        
        self.graphik = Graphik(self.gameDisplay)
        
        self.debug = False
        self.paused = False
        self.simCount = 0

        self.initializeSimulation()
        self.tickLengths = []
    
    def initializeSimulation(self):
        name = "Simulation " + str(self.simCount)
        self.simulation = Simulation(name, self.config, self.gameDisplay)
        self.simulation.initializeEntities()
        self.simulation.placeEntities()
        self.simulation.environment.printInfo()
        self.simCount += 1
        pygame.display.set_caption("Apex - " + name + " - " + str(self.simulation.environment.getGrid().getColumns()) + "x" + str(self.simulation.environment.getGrid().getRows()))
        
    def drawEnvironment(self):
        for location in self.simulation.environment.getGrid().getLocations():
            color = self.config.brown
            if location.getNumEntities() > 0:
                color = location.getEntities()[-1].getColor()
            self.graphik.drawRectangle(location.getX() * self.simulation.locationWidth, location.getY() * self.simulation.locationHeight, self.simulation.locationWidth, self.simulation.locationHeight, color)

    def displayStats(self):
        startingX = 50
        startingY = 50

        text = []

        if self.config.limitTickSpeed:
            text.append("Tick Speed:")
            text.append(str(self.config.tickSpeed))
            text.append("")
        text.append("Num Ticks:")
        text.append(str(self.simulation.numTicks))
        text.append("")
        text.append("Entities:")
        text.append(str(len(self.simulation.entities)))
        text.append("")
        text.append("Living Entities: ")
        text.append(str(self.simulation.getNumLivingEntities()))
        text.append("")
        text.append("Grass:")
        text.append(str(self.simulation.getNumberOfEntitiesOfType(Grass)))
        text.append("")
        text.append("Excrement:")
        text.append(str(self.simulation.getNumberOfEntitiesOfType(Excrement)))
        text.append("")
        text.append("Chickens:")
        text.append(str(self.simulation.getNumberOfLivingEntitiesOfType(Chicken)))
        text.append("")
        text.append("Pigs:")
        text.append(str(self.simulation.getNumberOfLivingEntitiesOfType(Pig)))
        text.append("")
        text.append("Cows:")
        text.append(str(self.simulation.getNumberOfLivingEntitiesOfType(Cow)))
        text.append("")
        text.append("Wolves:")
        text.append(str(self.simulation.getNumberOfLivingEntitiesOfType(Wolf)))
        text.append("")
        text.append("Foxes:")
        text.append(str(self.simulation.getNumberOfLivingEntitiesOfType(Fox)))

        buffer = self.config.textSize

        for i in range(0, len(text)):
            self.graphik.drawText(text[i], startingX, startingY + buffer*i, self.config.textSize, self.config.black)

    def handleKeyDownEvent(self, key):
        if key == pygame.K_d:
            if self.debug == True:
                self.debug = False
            else:
                self.debug = True
        if key == pygame.K_q:
            self.simulation.cleanup()
            self.simulation.running = False
        if key == pygame.K_r:
            self.simulation.cleanup()
            return "restart"
        if key == pygame.K_c:
            chicken = Chicken("player-created-chicken")
            self.simulation.environment.addEntity(chicken)
            self.simulation.addEntity(chicken)
        if key == pygame.K_p:
            pig = Pig("player-created-pig")
            self.simulation.environment.addEntity(pig)
            self.simulation.addEntity(pig)
        if key == pygame.K_m:
            cow = Cow("player-created-cow")
            self.simulation.environment.addEntity(cow)
            self.simulation.addEntity(cow)
        if key == pygame.K_w:
            wolf = Wolf("player-created-wolf")
            self.simulation.environment.addEntity(wolf)
            self.simulation.addEntity(wolf)
        if key == pygame.K_f:
            fox = Fox("player-created-fox")
            self.simulation.environment.addEntity(fox)
            self.simulation.addEntity(fox)
        if key == pygame.K_UP:
            if self.config.tickSpeed < self.config.maxTickSpeed:
                self.config.tickSpeed += 1
        if key == pygame.K_DOWN:
            if self.config.tickSpeed > 1:
                self.config.tickSpeed -= 1
        if key == pygame.K_l:
            if self.config.limitTickSpeed:
                self.config.limitTickSpeed = False
            else:
                self.config.limitTickSpeed = True
        if key == pygame.K_SPACE or key == pygame.K_ESCAPE:
            if self.paused:
                self.paused = False
            else:
                self.paused = True

    def restartSimulation(self):
        self.simulation.cleanup()
        self.tickLengths.append(self.simulation.numTicks)
        if self.config.reinitializeConfigUponRestart:
            self.config = Config()
        self.initializeSimulation()
        if self.paused:
            self.paused = False

    def getAverageTickLength(self):
        if len(self.tickLengths) == 0:
            return 0
        sum = 0
        for tickLength in self.tickLengths:
            sum += tickLength
        return sum/len(self.tickLengths)

    def quitApplication(self):
        self.simulation.cleanup()
        print("average simulation length:", self.getAverageTickLength(), "ticks")
        pygame.quit()
        quit()

    def simulationScreen(self):
        while self.simulation.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitApplication()
                elif event.type == pygame.KEYDOWN:
                    result = self.handleKeyDownEvent(event.key)
                    if result == "restart":
                        self.restartSimulation()
                elif event.type == pygame.VIDEORESIZE:
                    self.simulation.initializeLocationWidthAndHeight()
            
            if not self.paused:
                # update simulation
                self.simulation.update()

                # draw environment
                self.drawEnvironment()
                if self.debug:
                    self.displayStats()

            # update and sleep
            pygame.display.update()
            if (self.config.limitTickSpeed):
                time.sleep((self.config.maxTickSpeed - self.config.tickSpeed)/self.config.maxTickSpeed)
            
            # increment ticks if not paused
            if not self.paused:
                self.simulation.numTicks += 1
            
            # inform the user that we are paused if that is the case
            if self.paused:
                x, y = self.gameDisplay.get_size()
                self.graphik.drawText("PAUSED", x/2, y/2, 50, self.config.black)

            # check for zero living entities scenario
            if (self.config.endSimulationUponAllLivingEntitiesDying):
                if self.simulation.getNumLivingEntities() == 0:
                    self.running = False
                    time.sleep(1)
                    if (self.config.autoRestart):
                        self.restartSimulation()
                        
        # quit
        self.quitApplication()

    def run(self):
        self.simulationScreen()

apex = Apex()
apex.run()