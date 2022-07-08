# Copyright (c) 2022 Preponderous Software
# MIT License


# @author Daniel McCoy Stephenson
# @since July 1st, 2022
import datetime


class TimeSlot(object):

    def __init__(self, milliseconds):
        self.timestamp = datetime.datetime.now()
        self.milliseconds = milliseconds
        pass

    def getTimestamp(self):
        return self.timestamp
    
    def getMilliseconds(self):
        return self.milliseconds
    
    def setTimestamp(self, timestamp):
        self.timestamp = timestamp
    
    def setMilliseconds(self, milliseconds):
        self.milliseconds = milliseconds

    def isActive(self):
        return datetime.datetime.now() < self.timestamp + self.milliseconds