# Copyright (c) 2022 Preponderous Software
# MIT License
import datetime
import uuid
from lib.pyenvlib.entity import Entity
from lib.pyenvlib.grid import Grid


# @author Daniel McCoy Stephenson
# @since July 1st, 2022
class Environment(object):

    def __init__(self, name, size):
        self.id = uuid.uuid4()
        self.name = name
        self.grid = Grid(size, size)
        self.creationDate = datetime.datetime.now()
    
    def getID(self):
        return self.id
    
    def getName(self):
        return self.name

    def getCreationDate(self):
        return self.creationDate

    def getGrid(self):
        return self.grid

    def setID(self, id):
        self.id = id

    def setName(self, name):
        self.name = name

    def setGrid(self, grid):
        self.grid = grid

    def addEntity(self, entity: Entity):
        entity.setEnvironmentID(self.getID())
        success = False
        attempts = 100
        while (True):
            success = self.grid.addEntity(entity)
            attempts -= 1

            if (success):
                break
            elif (attempts == 0):
                print("Failed to add entity to environment")
                break
    
    def addEntityToLocation(self, entity: Entity, location):
        entity.setEnvironmentID(self.getID())
        self.grid.addEntityToLocation(entity, location)
    
    def removeEntity(self, entity: Entity):
        self.grid.removeEntity(entity)
    
    def isEntityPresent(self, entity: Entity):
        return self.grid.isEntityPresent(entity)

    def getNumEntities(self):
        return self.getGrid().getNumEntities()

    def printInfo(self):
        print("--------------")
        print(self.name)
        print("--------------")
        print("Num entities: ", self.getNumEntities())
        print("Num locations: ", self.getGrid().getSize())
        print("Creation Date: ", self.getCreationDate())
        print("ID: ", self.getID())
        print("Grid ID: ", self.getGrid().getID())
        print("\n")