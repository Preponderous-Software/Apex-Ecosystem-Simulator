import pygame
from lib.graphiklib.graphik import Graphik
from screen.mainMenuScreen import MainMenuScreen
from screen.screenType import ScreenType
from screen.simulationScreen import SimulationScreen
from simulation.config import Config

# @author Daniel McCoy Stephenson
# @since July 31st, 2022
class Apex:
    # constructors -----------------------------------------------------------
    def __init__(self):
        pygame.init()
        self.config = Config()
        self.__initializeGameDisplay()
        pygame.display.set_icon(pygame.image.load('src/media/icon/icon.PNG'))
        self.graphik = Graphik(self.gameDisplay)
        self.debug = False
        self.mainMenuScreen = MainMenuScreen(self.graphik)
        self.simulationScreen = SimulationScreen(self.graphik, self.config)
        self.currentScreen = self.mainMenuScreen

    # public methods ---------------------------------------------------------
    # Runs the application.
    def run(self):
        while True:
            result = self.currentScreen.run()
            if result == ScreenType.MAIN_MENU_SCREEN:
                return "restart"
            elif result == ScreenType.SIMULATION_SCREEN:
                self.currentScreen = self.simulationScreen
            elif result == ScreenType.NONE:
                self.__quitApplication()
            else:
                print("unrecognized screen: " + result)
                self.__quitApplication()

    # private methods --------------------------------------------------------
    def __initializeGameDisplay(self):
        if self.config.fullscreen:
            self.gameDisplay = pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.FULLSCREEN)
        else:
            self.gameDisplay = pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.RESIZABLE)

    # Shuts down the application.
    def __quitApplication(self):
        self.simulationScreen.simulation.cleanup()
        pygame.quit()
        quit()

apex = Apex()
apex.run()