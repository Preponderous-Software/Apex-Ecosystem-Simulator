# Copyright (c) 2022 Preponderous Software
# MIT License
import datetime
import uuid


# @author Daniel McCoy Stephenson
# @since July 1st, 2022
class Entity(object):

    def __init__(self, name):
        self.id = uuid.uuid4()
        self.name = name
        self.creationDate = datetime.datetime.now()
        self.environmentID = -1
        self.gridID = -1
        self.locationID = -1
    
    def getID(self):
        return self.id
    
    def getName(self):
        return self.name

    def getEnvironmentID(self):
        return self.environmentID

    def getCreationDate(self):
        return self.creationDate

    def getEnvironmentID(self):
        return self.environmentID

    def getGridID(self):
        return self.gridID

    def getLocationID(self):
        return self.locationID
    
    def setID(self, id):
        self.id = id

    def setName(self, name):
        self.name = name

    def setEnvironmentID(self, environmentID):
        self.environmentID = environmentID
    
    def setCreationDate(self, creationDate):
        self.creationDate = creationDate

    def setGridID(self, gridID):
        self.gridID = gridID

    def setLocationID(self, locationID):
        self.locationID = locationID
    
    def printInfo(self):
        print("--------------")
        print(self.name)
        print("--------------")
        print("ID: ", self.getID())
        print("Creation Date: ", self.getCreationDate())
        print("Environment ID: ", self.getEnvironmentID())
        print("Grid ID: ", self.getGridID())
        print("Location ID: ", self.getLocationID())
        print("\n")