import colours

import time

import pygame, math

class Robot(object):
    # Constructor for the Robot Class
    def __init__(self, speed, startPos, direction, colour):
        # Rect size to make the surface to draw the robot on
        rect = pygame.Rect((0, 0), (20, 20))

        self.colour = colour
        self.surf = pygame.Surface(rect.size, pygame.SRCALPHA)      # The surface the robot is drawn on
        self.surf.fill((255, 255, 255, 0))                          # Assigning it 'alpha' pixels which are used in bit mask collisions
        self.rect = pygame.draw.rect(self.surf, colour, rect)       # Drawing the robot on the surface as square
        self.mask = pygame.mask.from_surface(self.surf)             # bit mask used for collisions
        self.rect.centerx = self.centerx = float(startPos[0])       # centerx/centery:
        self.rect.centery = self.centery = float(startPos[1])       # are floats for more accurary oppose to ints which leads to
                                                                    # rounding errors and inaccurate location
        
        self.speed = float(speed)                                   # speed is pixels per second
        self.dest = None                                            # an (x, y) point the robot is heading toward
        self.angle = None                                           # angle oriented to either reach point or go around a ring
        self.direction = direction                                  # direction it goes around the ring
        self.onPerimeter = False                                    # if it found the perimeter yet or not
        self.evacuated = False                                      # if it found the exit yet or not
        self.ringPos = None                                         # the center of the ring
        self.travelled = []                                         # a list of points the robot has traveled

    # Finding a position in the grid and moves towards not already found
    # pos: (x,y) coordinate of the point
    # timeDelta: time since the last frame 
    def findPoint(self, pos, timeDelta):

        # If dest is not the pos to head towards, set it
        # The calculates the angle needed to head towards the point
        if not self.dest == pos:
            self.dest = (float(pos[0]), float(pos[1]))
            dx = self.dest[0] - self.centerx
            dy = self.dest[1] - self.centery

            self.angle = math.atan2(dy, dx)
            if self.angle < 0:
                self.angle += 2 * math.pi

        currDistance = self.checkDistance(self.dest)
        
        if len(self.travelled) > 0:
            lastPos = self.travelled[-1]
            if not (lastPos[0] == self.rect.centerx and lastPos[1] == self.travelled[-1]):
                self.travelled.append((self.rect.centerx, self.rect.centery))
        else:
            self.travelled.append((self.rect.centerx, self.rect.centery))

        newX = self.centerx + self.speed * timeDelta * math.cos(self.angle)
        newY = self.centery + self.speed * timeDelta * math.sin(self.angle)

        newDistance = self.checkDistance((newX, newY))

        if currDistance > newDistance:
            self.centerx = newX
            self.centery = newY
        else:
            self.centerx = pos[0]
            self.centery = pos[1]

        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

        return (currDistance - newDistance) < 0

    def collision(self, destination):
        dx = self.rect.centerx - destination.rect.centerx
        dy = self.rect.centery - destination.rect.centery

        area1 = self.mask.scale(destination.rect.size).overlap_area(destination.mask,(dx, dy))
        area2 = self.mask.scale(destination.rect.size).overlap_area(destination.mask,(-dx, -dy))
        area3 = self.mask.scale(destination.rect.size).overlap_area(destination.mask,(-dx, dy))
        area4 = self.mask.scale(destination.rect.size).overlap_area(destination.mask,(dx, -dy))
        
        return max([ area1, area2, area3, area4 ])

    def findExitOnRing(self, ring, timeDelta):
        if not self.ringPos == (ring.rect.centerx, ring.rect.centery):
            self.ringPos = (float(ring.rect.centerx), float(ring.rect.centery))
            dx = self.centerx - self.ringPos[0]
            dy = self.centery - self.ringPos[1]

            self.angle = math.atan2(dy, dx)
            if self.angle < 0:
                self.angle += 2 * math.pi

        currMaxArea = newMaxArea = 0

        if len(self.travelled) > 0:
            lastPos = self.travelled[-1]
            if not (lastPos[0] == self.rect.centerx and lastPos[1] == self.travelled[-1]):
                self.travelled.append((self.rect.centerx, self.rect.centery))
        else:
            self.travelled.append((self.rect.centerx, self.rect.centery))

        collided = self.rect.colliderect(ring.exit.rect)
        if collided:
            currMaxArea = self.collision(ring.exit)

        self.angle += self.direction * timeDelta * (self.speed / ring.radius)
        self.rect.centerx = self.centerx = ring.radius * math.cos(self.angle) + self.ringPos[0]
        self.rect.centery = self.centery = ring.radius * math.sin(self.angle) + self.ringPos[1]

        if collided:
            newMaxArea = self.collision(ring.exit)

        return currMaxArea > newMaxArea and not currMaxArea == 0

    def checkDistance(self, point):
        return math.sqrt((self.centerx- point[0]) ** 2 + (self.centery - point[1]) ** 2)

    def drawRobot(self, surface):
        surface.blit(self.surf, self.rect)

    def drawTravelledLine(self, surface):
        if len(self.travelled) > 1:
            pygame.draw.lines(surface, self.colour, False, self.travelled, 3)