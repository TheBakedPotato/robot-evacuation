import pygame

class Line(object):
    # Constructor for the Line class
    def __init__(self, slope, yInt=None):
        self.slope = slope          # Slope of the line

        if yInt:
            self.yInt = yInt        # y-intercept of the line

    # Another constructor to construct a line based off 2 points
    # point1: (x, y) coordinate
    # point2: (x, y) coordinate
    # returns the new Line object
    @classmethod
    def fromPoints(cls, point1, point2):
        # Checks to see if their x positions are the same. If they are, the slope is undefined
        if point1[0] == point2[0]:
            slope = None
        else:
            slope = (float(point2[1]) - point1[1]) / (float(point2[0]) - point1[0])
        
        obj = cls(slope)
        obj.yInt = obj.findIntercept(point1)

        return obj

    # Another constructor to construct a line based off a slope and a point
    # point: (x, y) coordinate
    # slope: the slope of the line
    # returns the new Line object
    @classmethod
    def fromSlopeAndPoint(cls, slope, point):
        obj = cls(slope)
        obj.yInt = obj.findIntercept(point)
        return obj

    # Returns the y-intercept for a line that only has a slope
    # point: (x,y) coordinate
    def findIntercept(self, point):
        return point[1] - float(point[0]) * self.slope