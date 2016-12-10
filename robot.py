import colours

import pygame, math

class Robot:
    def __init__(self, speed, startPos):
        rect = pygame.Rect((0, 0), (20, 20))

        self.speed = (speed, speed)
        self.surf = pygame.Surface(rect.size)
        self.rect = pygame.draw.rect(self.surf, colours.BLACK, rect)
        self.rect.centerx = startPos[0]
        self.rect.centery = startPos[1]

        self._moving = False
        self._moveX = 0
        self._moveY = 0

    def findPerimeter(self, start, radius, timeDelta, angle):
        if not self._moving:
            self._moving = True
            self._moveX = 0
            self._moveY = 0

        self._moveX += self.speed[0] * timeDelta * math.cos(math.radians(angle))
        self._moveY += self.speed[1] * timeDelta * math.sin(math.radians(angle))

        if (self._moveX >= 1) or (self._moveX <= -1):  
            self.rect = self.rect.move(self._moveX, 0)
            self._moveX = 0

        if (self._moveY >= 1) or (self._moveY <= -1):
            self.rect = self.rect.move(0, self._moveY)
            self._moveY = 0

        return math.sqrt((self.rect.centerx - start[0]) ** 2 + (self.rect.centery - start[1]) ** 2) >= radius
