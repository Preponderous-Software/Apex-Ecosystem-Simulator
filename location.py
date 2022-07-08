# Copyright (c) 2022 Preponderous Software
# MIT License


# @author Daniel McCoy Stephenson
# @since July 1st, 2022
import random
from re import X

from entity import Entity


class Location(object):

    def __init__(self, x, y, parentGrid):
        self.id = random.randint(0, 999) # TODO: make this unique
        self.x = x
        self.y = y
        self.parentGrid = parentGrid
        self.entities = []
    
    def getID(self):
        return self.id
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getParentGrid(self):
        return self.parentGrid

    def getNumEntities(self):
        return len(self.entities)
    
    def addEntity(self, entity: Entity):
        self.entities.append(entity)
        entity.setLocationID(self.getID())
    
    def removeEntity(self, entity: Entity):
        self.entities.remove(entity)
    
    def isEntityPresent(self, entity: Entity):
        return entity in self.entities