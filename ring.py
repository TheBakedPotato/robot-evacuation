import pygame, random, math

import colours, destination

class Ring(object):
    # Constructor for the Ring class
    def __init__(self, pos, radius, exitPos=None):
        self.pos = pos                              # Location for the center of the ring
        self.radius = radius                        # Radius of the ring

        # Setting up the surface of the ring and getting its rect
        rect = pygame.Rect((0, 0), (self.radius * 2, self.radius * 2))
        self.surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.surf.fill((255, 255, 255, 0))
        pygame.draw.circle(self.surf, colours.BLACK, (self.radius, self.radius), self.radius, 1)
        self.rect = self.surf.get_rect()

        # Positition the ring based on the given position
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

        # Setting the exit of the ring
        self.exit = destination.Destination(self.pointOnRing())

    # Draws the ring and its exit on a surface
    # surface: the Surface to draw the ring on
    def draw(self, surface):
        surface.blit(self.surf, self.rect)
        self.exit.draw(surface)

    # Finds a point on the perimeter of the ring at a given angle
    # angle: The angle in radians
    # returns the point as (x,y)
    def pointOnRingAngle(self, angle):
        x = self.pos[0] + self.radius * math.cos(angle)
        y = self.pos[1] + self.radius * math.sin(angle)
        return (x, y)

    # Returns a random point on the perimeter of the ring in the form (x,y)
    def pointOnRing(self):
        angle = (2 * math.pi) * random.random()
        return self.pointOnRingAngle(angle)

    # Finds a point in the body of the ring at a given angle
    # angle: The angle in radians
    # returns the point as (x,y)    
    def pointInRingAngle(self, angle):
        # A point in the ring is just a point on the perimeter of a circle with a smaller radius
        tempRadius = self.radius * random.random()
        x = self.pos[0] + tempRadius * math.cos(angle)
        y = self.pos[1] + tempRadius * math.sin(angle)
        return (x, y)

    # Returns a random point in the body of the ring in the form (x,y)
    def pointInRing(self):
        angle = (2 * math.pi) * random.random()
        return self.pointInRingAngle(angle)

    # Returns the point(s) where a Line intersects with the ring
    # line: the Line to check the intersection with
    # returns the points in an array
    def intersectionWithLine(self, line):
        a = line.slope ** 2 + 1
        b = 2 * (line.slope * line.yInt - line.slope * self.pos[1] - self.pos[0])
        c = (self.pos[1] ** 2) - (self.radius ** 2) + (self.pos[0] ** 2) - (2 * line.yInt * self.pos[1]) + (line.yInt ** 2)

        radical = (b ** 2) - (4 * a * c)
        if radical < 0:
            return []

        x1 = ((-b) + math.sqrt(radical)) / (2 * a)
        x2 = ((-b) - math.sqrt(radical)) / (2 * a)

        y1 = line.slope * x1 + line.yInt
        y2 = line.slope * x2 + line.yInt

        return [(x1, y1), (x2, y2)]