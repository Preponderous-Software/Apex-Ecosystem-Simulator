import os
import time
import pygame

from entity.chicken import Chicken
from entity.cow import Cow
from entity.fox import Fox
from entity.grass import Grass
from entity.livingEntity import LivingEntity
from entity.pig import Pig
from entity.rabbit import Rabbit
from entity.wolf import Wolf
from lib.graphiklib.graphik import Graphik
from screen.screenType import ScreenType
from simulation.config import Config
from simulation.simulation import Simulation
from ui.textAlertDrawTool import TextAlertDrawTool
from ui.textAlertFactory import TextAlertFactory

# @author Daniel McCoy Stephenson
class SimulationScreen:
    # constructors -----------------------------------------------------------
    def __init__(self, graphik: Graphik, config: Config):
        self.__graphik = graphik
        self.getConfig() = config
        self.__nextScreen = ScreenType.NONE
        self.__changeScreen = False
        self.__paused = False
        self.__debug = False
        self.__textAlerts = []
        self.__textAlertFactory = TextAlertFactory()
        self.__textAlertDrawTool = TextAlertDrawTool()
        self.__selectedEntity = None
    
    # public methods ---------------------------------------------------------
    # Invokes the simulation screen loop.
    def run(self):
        while not self.__changeScreen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__nextScreen = ScreenType.NONE
                    self.__changeScreen = True
                    break
                elif event.type == pygame.KEYDOWN:
                    self.__handleKeyDownEvent(event.key)
                elif event.type == pygame.VIDEORESIZE:
                    self.simulation.initializeLocationWidthAndHeight()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.getConfig().localView == False:
                    self.__handleMouseClickEvent(event.pos)
            
            if not self.__paused:
                self.simulation.update()
                self.__graphik.gameDisplay.fill(self.getConfig().black)
                if self.simulation.getNumLivingEntities() != 0:
                    if self.getConfig().localView and self.__selectedEntity != None:
                        self.__drawAreaAroundSelectedEntity()
                    else:
                        self.__drawEnvironment()

                    if self.__debug:
                        self.__displayStats()
            
            self.__drawTextAlerts()
            
            # if selected entity is no longer alive, deselect it
            if self.__selectedEntity != None and not self.simulation.environment.isEntityPresent(self.__selectedEntity):
                self.__selectedEntity = None
                
                # if local view, switch back to global view
                if self.getConfig().localView:
                    self.getConfig().localView = False

            self.__drawVersion()
            pygame.display.update()
            if (self.getConfig().limitTickSpeed):
                time.sleep((self.getConfig().maxTickSpeed - self.getConfig().tickSpeed)/self.getConfig().maxTickSpeed)
            
            if not self.__paused:
                self.simulation.numTicks += 1
            
            if self.__paused:
                x, y = self.__graphik.gameDisplay.get_size()
                self.__graphik.drawText("PAUSED", x/2, y/2, 50, self.getConfig().black)

            if (self.getConfig().endSimulationUponAllLivingEntitiesDying):
                if self.simulation.getNumLivingEntities() == 0:
                    time.sleep(1)
                    self.simulation.cleanup()
                    if self.getConfig().randomizeGridSizeUponRestart:
                        self.getConfig().randomizeGridSize()
                        self.getConfig().randomizeGrassGrowTime()
                        self.getConfig().calculateValues()
                    self.__nextScreen = ScreenType.SETUP_SCREEN
                    self.__changeScreen = True
                    if self.__paused:
                        self.__paused = False

        
        self.__changeScreen = False
        return self.__nextScreen
    
    def initializeSimulation(self):
        name = "Simulation"
        self.simulation = Simulation(name, self.getConfig(), self.__graphik.gameDisplay)
        self.simulation.generateInitialEntities()
        self.simulation.placeInitialEntitiesInEnvironment()
        self.simulation.environment.printInfo()
        self.__initializeCaption()

    # private methods --------------------------------------------------------
    def __initializeCaption(self):
        caption = "Apex - " + self.simulation.name + " - " + str(self.simulation.environment.getGrid().getColumns()) + "x" + str(self.simulation.environment.getGrid().getRows())
        if self.getConfig().muted:
            caption += " (muted)"
        pygame.display.set_caption(caption)

    def __drawVersion(self):
        if os.path.isfile("version.txt"):
            with open("version.txt", "r") as file:
                version = file.read()

                # display centered at bottom of screen
                self.__graphik.drawText(
                    version,
                    self.__graphik.getGameDisplay().get_size()[0] / 2,
                    self.__graphik.getGameDisplay().get_size()[1] - 10,
                    16,
                    (255, 255, 255),
                )

    # Draws the environment that belongs to the simulation in its entirety.
    def __drawEnvironment(self):
        for locationId in self.simulation.environment.getGrid().getLocations():
            location = self.simulation.environment.getGrid().getLocations()[locationId]
            self.__drawLocation(location, location.getX() * self.simulation.locationWidth - 1, location.getY() * self.simulation.locationHeight - 1, self.simulation.locationWidth + 2, self.simulation.locationHeight + 2)

    # Draws a location at a specified position.
    def __drawLocation(self, location, xPos, yPos, width, height):
        color = self.__getColorOfLocation(location)
        self.__graphik.drawRectangle(xPos, yPos, width, height, color)
        if self.getConfig().eyesEnabled and location != -1 and self.__locationContainsLivingEntity(location):
            eyeSizeFactor = 0.25
            pupilSizeFactor = 0.5
            self.__drawEyes(xPos, yPos, width, height, eyeSizeFactor, pupilSizeFactor)

    # Returns the color that a location should be displayed as.
    def __getColorOfLocation(self, location):
        if location == -1:
            color = self.getConfig().black
        else:
            color = self.getConfig().brown
            if location.getNumEntities() > 0:
                topEntityId = list(location.getEntities().keys())[-1]
                topEntity = location.getEntities()[topEntityId]
                oldestLivingEntityId = self.simulation.livingEntityIds[0]
                oldestLivingEntity = self.simulation.entities[oldestLivingEntityId]
                if self.getConfig().highlightOldestEntity and topEntity.getID() == oldestLivingEntity.getID():
                    color = self.getConfig().highlightColor
                else:
                    color = topEntity.getColor()
        return color

    def __locationContainsLivingEntity(self, location):
        if location.getNumEntities() == 0:
            return False
        topEntityId = list(location.getEntities().keys())[-1]
        topEntity = location.getEntities()[topEntityId]
        return location.getNumEntities() > 0 and isinstance(topEntity, LivingEntity)

    def __drawEyes(self, xPos, yPos, width, height, eyeSizeFactor, pupilSizeFactor):
        # draw eyes
        leftEyeXPos = xPos + width/8
        leftEyeYPos = yPos + height/4
        leftEyeWidth = width*eyeSizeFactor
        leftEyeHeight = height*eyeSizeFactor
        self.__graphik.drawRectangle(leftEyeXPos, leftEyeYPos, leftEyeWidth, leftEyeHeight, self.getConfig().white)
        
        rightEyeXPos = xPos + width/2
        rightEyeYPos = yPos + height/4
        rightEyeWidth = width*eyeSizeFactor
        rightEyeHeight = height*eyeSizeFactor
        self.__graphik.drawRectangle(rightEyeXPos, rightEyeYPos, rightEyeWidth, rightEyeHeight, self.getConfig().white)
        
        # draw pupils            
        leftPupilXPos = leftEyeXPos + leftEyeWidth/4
        leftPupilYPos = leftEyeYPos + leftEyeHeight/4
        leftPupilWidth = leftEyeWidth*pupilSizeFactor
        leftPupilHeight = leftEyeHeight*pupilSizeFactor
        self.__graphik.drawRectangle(leftPupilXPos, leftPupilYPos, leftPupilWidth, leftPupilHeight, self.getConfig().black)
        
        rightPupilXPos = rightEyeXPos + rightEyeWidth/4
        rightPupilYPos = rightEyeYPos + rightEyeHeight/4
        rightPupilWidth = rightEyeWidth*pupilSizeFactor
        rightPupilHeight = rightEyeHeight*pupilSizeFactor
        self.__graphik.drawRectangle(rightPupilXPos, rightPupilYPos, rightPupilWidth, rightPupilHeight, self.getConfig().black)

    # Draws the immediate area around the selected entity.
    def __drawAreaAroundSelectedEntity(self):
        locationID = self.__selectedEntity.getLocationID()
        grid = self.simulation.environment.getGrid()
        location = grid.getLocation(locationID)
        x, y = self.gameDisplay.get_size()
        width = x/(self.getConfig().localViewSize*2 + 1)
        height = y/(self.getConfig().localViewSize*2 + 1)
        xpos = width*self.getConfig().localViewSize
        ypos = height*self.getConfig().localViewSize
        yBackup = ypos
        self.__drawRow(location, grid, xpos, ypos, width, height)
        self.__drawRowsAboveLocation(location, grid, xpos, ypos, width, height)
        ypos = yBackup
        self.__drawRowsBelowLocation(location, grid, xpos, ypos, width, height)

    # Draws locations to the left of a given location.
    def __drawLocationsToTheLeftOfLocation(self, location, grid, xpos, ypos, width, height):
        tempLoc = location
        while tempLoc != -1:
            xpos = xpos - width
            ypos = ypos
            self.__drawLocation(grid.getLeft(tempLoc), xpos, ypos, width, height)
            tempLoc = grid.getLeft(tempLoc)
    
    # Draws locations to the right of a given location.
    def __drawLocationsToTheRightOfLocation(self, location, grid, xpos, ypos, width, height):
        tempLoc = location
        while tempLoc != -1:
            xpos = xpos + width
            ypos = ypos
            self.__drawLocation(grid.getRight(tempLoc), xpos, ypos, width, height)
            tempLoc = grid.getRight(tempLoc)
    
    # Draws a row of locations starting at a given location.
    def __drawRow(self, location, grid, xpos, ypos, width, height):
        self.__drawLocation(location, xpos, ypos, width, height)
        xBackup = xpos
        self.__drawLocationsToTheLeftOfLocation(location, grid, xpos, ypos, width, height)
        xpos = xBackup
        self.__drawLocationsToTheRightOfLocation(location, grid, xpos, ypos, width, height)
    
    # Draws rows of locations starting above a given location.
    def __drawRowsAboveLocation(self, location, grid, xpos, ypos, width, height):
        nextLocation = grid.getUp(location)
        while nextLocation != -1:
            ypos = ypos - height
            self.__drawRow(nextLocation, grid, xpos, ypos, width, height)
            nextLocation = grid.getUp(nextLocation)

    # Draws rows of locations starting below a given location.
    def __drawRowsBelowLocation(self, location, grid, xpos, ypos, width, height):
        nextLocation = grid.getDown(location)
        while nextLocation != -1:
            ypos = ypos + height
            self.__drawRow(nextLocation, grid, xpos, ypos, width, height)
            nextLocation = grid.getDown(nextLocation)

    def __drawTextAlerts(self):
        for textAlert in self.__textAlerts:
            self.__textAlertDrawTool.drawTextAlert(textAlert, self.__graphik)
            textAlert.duration -= 1
            if textAlert.duration == 0:
                self.__textAlerts.remove(textAlert)

    # Draws some statistics to the screen, which are updated each tick. This can be laggy.
    def __displayStats(self):
        startingX = 100
        startingY = 10
        text = []
        if self.getConfig().limitTickSpeed:
            self.__addStatToText(text, "Tick Speed:", str(self.getConfig().tickSpeed))
        self.__addStatToText(text, "Num Ticks:", str(self.simulation.numTicks))
        self.__addStatToText(text, "Entities:", str(len(self.simulation.entities)))
        self.__addStatToText(text, "Living Entities:", str(self.simulation.getNumLivingEntities()))
        self.__addStatToText(text, "Grass:", str(self.simulation.getNumberOfEntitiesOfType(Grass)))
        self.__addStatToText(text, "Excrement:", str(self.simulation.getNumExcrement()))
        self.__addStatToText(text, "Chickens:", str(self.simulation.getNumberOfLivingEntitiesOfType(Chicken)))
        self.__addStatToText(text, "Pigs:", str(self.simulation.getNumberOfLivingEntitiesOfType(Pig)))
        self.__addStatToText(text, "Cows:", str(self.simulation.getNumberOfLivingEntitiesOfType(Cow)))
        self.__addStatToText(text, "Wolves:", str(self.simulation.getNumberOfLivingEntitiesOfType(Wolf)))
        self.__addStatToText(text, "Foxes:", str(self.simulation.getNumberOfLivingEntitiesOfType(Fox)))
        self.__addStatToText(text, "Rabbits:", str(self.simulation.getNumberOfLivingEntitiesOfType(Rabbit)))

        buffer = self.getConfig().textSize

        for i in range(0, len(text)):
            self.__graphik.drawText(text[i], startingX, startingY + buffer*i, self.getConfig().textSize, self.getConfig().black)

    def __addStatToText(self, text, key, value):
        text.append(key)
        text.append(value)
        text.append("")

    # Defines the controls of the application.
    def __handleKeyDownEvent(self, key):
        if key == pygame.K_d:
            if self.__debug == True:
                self.__debug = False
            else:
                self.__debug = True
        if key == pygame.K_q:
            self.simulation.cleanup()
            self.simulation.running = False
        if key == pygame.K_r:
            self.simulation.cleanup()
            return "restart"
        if key == pygame.K_c:
            chicken = Chicken("player-created-chicken")
            self.simulation.environment.addEntity(chicken)
            self.simulation.addEntityToTrackedEntities(chicken)
        if key == pygame.K_p:
            pig = Pig("player-created-pig")
            self.simulation.environment.addEntity(pig)
            self.simulation.addEntityToTrackedEntities(pig)
        if key == pygame.K_k:
            cow = Cow("player-created-cow")
            self.simulation.environment.addEntity(cow)
            self.simulation.addEntityToTrackedEntities(cow)
        if key == pygame.K_w:
            wolf = Wolf("player-created-wolf")
            self.simulation.environment.addEntity(wolf)
            self.simulation.addEntityToTrackedEntities(wolf)
        if key == pygame.K_f:
            fox = Fox("player-created-fox")
            self.simulation.environment.addEntity(fox)
            self.simulation.addEntityToTrackedEntities(fox)
        if key == pygame.K_b:
            rabbit = Rabbit("player-created-rabbit")
            self.simulation.environment.addEntity(rabbit)
            self.simulation.addEntityToTrackedEntities(rabbit)
        if key == pygame.K_RIGHTBRACKET:
            if self.getConfig().tickSpeed < self.getConfig().maxTickSpeed:
                self.getConfig().tickSpeed += 1
        if key == pygame.K_LEFTBRACKET:
            if self.getConfig().tickSpeed > 1:
                self.getConfig().tickSpeed -= 1
        if key == pygame.K_l:
            if self.getConfig().limitTickSpeed:
                self.getConfig().limitTickSpeed = False
            else:
                self.getConfig().limitTickSpeed = True
        if key == pygame.K_SPACE or key == pygame.K_ESCAPE:
            if self.__paused:
                self.__paused = False
            else:
                self.__paused = True
        if key == pygame.K_v:
            if self.getConfig().localView:
                self.getConfig().localView = False
            else:
                self.getConfig().localView = True
        if key == pygame.K_h:
            if self.getConfig().highlightOldestEntity:
                self.getConfig().highlightOldestEntity = False
            else:
                self.getConfig().highlightOldestEntity = True
        if key == pygame.K_UP:
            if self.getConfig().localViewSize < self.getConfig().maxLocalViewSize:
                self.getConfig().localViewSize += 1
        if key == pygame.K_DOWN:
            if self.getConfig().localViewSize > 1:
                self.getConfig().localViewSize -= 1
        if key == pygame.K_F11:
            if self.getConfig().fullscreen:
                self.getConfig().fullscreen = False
            else:
                self.getConfig().fullscreen = True
            self.initializeGameDisplay()
        if key == pygame.K_m:
            if self.getConfig().muted:
                self.getConfig().muted = False
            else:
                self.getConfig().muted = True
            self.__initializeCaption()
        if key == pygame.K_e:
            if self.getConfig().eyesEnabled:
                self.getConfig().eyesEnabled = False
            else:
                self.getConfig().eyesEnabled = True

    def __retrieveLocationAtMousePosition(self, pos):
        x, y = pos
        grid = self.simulation.environment.getGrid()
        locationWidth = self.simulation.locationWidth
        locationHeight = self.simulation.locationHeight
        locationX = x // locationWidth
        locationY = y // locationHeight
        location = grid.getLocationByCoordinates(locationX, locationY)
        return location
                
    def __handleMouseClickEvent(self, pos):
        location = self.__retrieveLocationAtMousePosition(pos)
        if location != -1:
            self.__printLocationInfoToConsole(location)
            self.__createTextAlertForLocationInfo(location)
            pygame.display.update()
            if location.getNumEntities() > 0:
                topEntity = location.getEntities()[list(location.getEntities().keys())[-1]]
                if isinstance(topEntity, LivingEntity):
                    self.__selectedEntity = topEntity
                else:
                    self.__selectedEntity = None

    def __createTextAlertForLocationInfo(self, location):
        newAlert = self.__textAlertFactory.createTextAlertForLocationInfo(location, self.simulation, self.getConfig())
        self.__textAlerts.append(newAlert)

    def __printLocationInfoToConsole(self, location):
        if location != -1:
            print("")
            print("=== Location (" + str(location.getX()) + ", " + str(location.getY()) + ") ===")
            print("Number of entities: " + str(location.getNumEntities()))
            entityNames = []
            for entityId in location.getEntities():
                entity = location.getEntities()[entityId]
                entityNames.append(entity.getName())
            # print occurrences
            for entityName in set(entityNames):
                print(entityName + ": " + str(entityNames.count(entityName)))
            print("")