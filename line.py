import pygame

class Line(object):
    def __init__(self, slope, yInt=None):
        self.slope = slope

        if yInt:
            self.yInt = yInt

    @classmethod
    def fromPoints(cls, point1, point2):
        if point1[0] == point2[0]:
            slope = None
        else:
            slope = (float(point2[1]) - point1[1]) / (float(point2[0]) - point1[0])
        
        obj = cls(slope)
        obj.yInt = obj.findIntercept(point1)

        return obj

    @classmethod
    def fromSlopeAndPoint(cls, slope, point):
        obj = cls(slope)
        obj.yInt = obj.findIntercept(point)
        return obj

    def findIntercept(self, point):
        return point[1] - float(point[0]) * self.slope