import pygame

class Line:
    def __init__(slope, yInt=None):
        self.slope = slope

        if yInt:
            self.yInt = yInt

    @classmethod
    def fromPoints(self, point1, point2):
        if point1[0] == point2[0]:
            slope = None
        else:
            slope = (float(point2[1]) - point1[1]) / (float(point2[0]) - point1[0])
        
        yInt = self.findIntercept(point1)

        return self(slope, yInt)


    def findIntercept(self, point):
        return point[1] - float(point[0]) * slope