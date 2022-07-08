# Copyright (c) 2022 Preponderous Software
# MIT License


# @author Daniel McCoy Stephenson
# @since July 1st, 2022
import random

from entity import Entity
from location import Location


class Grid(object):

    def __init__(self, columns, rows, parentEnvironment):
        self.id = random.randint(0, 999) # TODO: make this unique
        self.columns = columns
        self.rows = rows
        self.parentEnvironment = parentEnvironment
        self.locations = []
        self.generateLocations()

    def getID(self):
        return self.id

    def getColumns(self):
        return self.columns

    def getRows(self):
        return self.rows
    
    def getParentEnvironment(self):
        return self.parentEnvironment

    def getLocations(self):
        return self.locations

    def getFirstLocation(self):
        return self.locations[0]

    def getSize(self):
        return len(self.locations)
    
    def getLocations(self):
        return self.locations
    
    def getNumEntities(self):
        count = 0
        for location in self.locations:
            count += location.getNumEntities()
        return count
    
    def setID(self, id):
        self.id = id
    
    def setColumns(self, columns):
        self.columns = columns;
    
    def setRows(self, rows):
        self.rows = rows;
    
    def setParentEnvironment(self, parentEnvironment):
        self.parentEnvironment = parentEnvironment
    
    def setLocations(self, locations):
        self.locations = locations
    
    def addLocation(self, location):
        self.locationss.append(location)
    
    def removeLocation(self, location):
        self.locations.remove(location)
    
    def addEntity(self, entity: Entity):
        self.getFirstLocation().addEntity(entity)
        entity.setGridID(self.getID())
    
    def removeEntity(self, entity: Entity):
        for location in self.grid.getLocations():
            if location.isEntityPresent(entity):
                location.removeEntity(entity)
                return
    
    def isEntityPresent(self, entity: Entity):
        for location in self.grid.getLocations():
            if location.isEntityPresent(entity):
                return True

    def generateLocations(self):
        for x in range(self.getColumns()):
            for y in range(self.getRows()):
                location = Location(x, y, self)
                self.locations.append(location)
